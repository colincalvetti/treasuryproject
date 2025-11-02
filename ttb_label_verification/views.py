from django.shortcuts import render
from ttb import forms
import base64
from django.http import JsonResponse
import json
import pytesseract as ocr
from PIL import Image
import io
from google import genai
from google.genai import types
import os

def home(request):
    if(request.method == 'POST'):
        if 'verification_status' in request.POST:
            verification_status = request.POST.get('verification_status')
            form = forms.CreateTTB(initial={
                'brand': request.POST.get('brand'),
                'alcohol_type': request.POST.get('alcohol_type'),
                'abv': request.POST.get('abv'),
                'volume': request.POST.get('volume'),
                'v_units': request.POST.get('v_units'),
                'origin': request.POST.get('origin'),
                'bottler': request.POST.get('bottler'),
                'bottler_address': request.POST.get('bottler_address'),
                'age': request.POST.get('age'),
                'health_warnings': request.POST.get('health_warnings'),
            })
            form.fields['image'].required = False
            form.fields['image'].help_text = '<span style="color: red;"><br>Image Upload Not Required when Editing</span>'
            image = request.POST.get('image')
            return render(request, 'home.html', {'form': form,'image':image,'verification_status':verification_status,'edit':True})

        form = forms.CreateTTB(request.POST,request.FILES)
        if not 'image' in request.FILES:
            form.fields['image'].required = False
        if(form.is_valid()):
            ttb = form.save(commit=False)
            image = None
            if 'image' in request.FILES:
                image_upload = request.FILES['image']
                image_data = base64.b64encode(image_upload.read()).decode('utf-8')
                image_mime = image_upload.content_type
                image = f"data:{image_mime};base64,{image_data}"
            else:
                image = request.POST.get('image')
            return render(request,'home.html',{'ttb':ttb,'image':image})
    else:
        form = forms.CreateTTB()
    return render(request,'home.html',{'form':form})

def ttb_verification(request):
    if(request.method == 'POST'):
        data = json.loads(request.body)
        ttbData = {
            "brand": data["brand"],
            "alcohol_type": data["alcohol_type"],
            "abv": data["abv"],
            "volume": data["volume"],
            "v_units": data["v_units"],
            "origin": data["origin"],
            "bottler": data["bottler"],
            "bottler_address": data["bottler_address"],
            "age": data["age"],
            "health_warnings": data["health_warnings"],
        }

        systemprompt = (
            "You are a TTB verification agent. Your task is to determine if the provided TTB label information matches the provided image of the label."
            +"\nAnalyze the image and compare it with the provided data: TTB Data: brand, alcohol type, abv, volume, origin, bottler, bottler address, age, and health warnings. Use the provided pdf for a more extensive list of TTB labeling requirements."
            +"\nFormulate a detailed assessment of whether the information is accurate or not. Respond with 'verified' and a confidence percentage if all information matches along with a short explanation of teh reason for the provided confidence percentage, otherwise respond with 'not verified' and include a short description of the discrepancies. Clearly and Concisely list discrepancies."
            +"\nFormat reponse in the following format if verified: xx% confidence that TTB label matches image \n\n <explanation of chosen confidence percentage>"
            +"\nFormat reponse in the following format if not verified: TTB label does not match image \n\n discrepancy category 1: discrepancy explanation 1 \n\n discrepancy category 2: discrepancy explanation 2 \n\n ... \n\n discrepancy category n: discrepancy explanation n"
        )
        userprompt = (
            "TTB Data: "+json.dumps(ttbData)
        )

        pdf_bytes = None
        with open('ttb_requirements.pdf', 'rb') as f:
            pdf_bytes = f.read()

        header, encoded = data['image'].split(",", 1)
        mime_type = header.split(":")[1].split(";")[0]
        image_bytes = base64.b64decode(encoded)

        api_key = os.getenv("G_API_KEY")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                ['system',systemprompt],
                ['user',userprompt],
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                ),
                types.Part.from_bytes(
                    data=pdf_bytes,
                    mime_type='application/pdf',
                )
            ]
        )
        client.close()

        unformatted_response = response.text
        formatted_response = (
            unformatted_response.replace("* **", "\n\n")
            .replace(":**", ":")
            .strip()
        )

        return JsonResponse({"ttb_status":formatted_response})