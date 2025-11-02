from django.db import models
from django.core.validators import FileExtensionValidator

class TTB(models.Model):
    image = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    brand = models.CharField(max_length=255)
    alcohol_type = models.CharField(max_length=6,choices=(('Beer','Beer'),('Wine','Wine'),('Liquor','Liquor')))
    abv = models.DecimalField(max_digits=5,decimal_places=2)
    volume = models.DecimalField(max_digits=5,decimal_places=2)
    v_units = models.CharField(max_length=5,choices=(('mL','mL'),('L','L'),('fl oz','fl oz')))
    origin = models.CharField(max_length=255)
    bottler = models.CharField(max_length=255)
    bottler_address = models.CharField(max_length=255)
    age = models.CharField(max_length=50)
    health_warnings = models.CharField(max_length=510)