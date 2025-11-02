# To run application locally on Mac/Linux or Windows:

## 1. Obtain free Google Generative AI API Key from [Google AI Studio](https://aistudio.google.com/u/1/api-keys)

## 2. Set API key as an evironment variable:
**Mac/Linux:**
```bash
export G_API_KEY=<api key>
```
**Windows:**
```bash
setx G_API_KEY "<api key>"
```

## 3. Obtain Source Code
```bash
git pull git@github.com:colincalvetti/treasuryproject.git
```

## 4. Create Virtual Environment
```bash
python -m venv <virtual environment name>
```

## 5. Activate Virtual Environment
**Mac/Linux:**
```bash
source <virtual environment name>/bin/activate
```
**Windows Powershell:**
```bash
<virtual environment name>\Scripts\Activate.ps1
```
**Windows Command Prompt:**
```bash
<virtual environment name>\Scripts\activate.bat
```

## 6. Navigate to Project Root Directory
```bash
cd <project root directory name>
```

## 7. Install Required Python Modules
```bash
pip install -r requirements.txt
```

## 8. Run the Program
```bash
python manage.py runserver
```

## 9. Open Link from Terminal Output in Browser
[Open Localhost in Browser](http://127.0.0.1:8000/)