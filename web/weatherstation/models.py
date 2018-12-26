from django.db import models

# Create your models here.
class Measurement(models.Model):
    date = models.DateTimeField(null=False)
    temperature = models.DecimalField(null=True)
    humidity = models.DecimalField(null=True)
    
    def __str__(self):
        return str(self.humidity)