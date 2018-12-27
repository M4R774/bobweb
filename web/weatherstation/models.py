from django.db import models


# Create your models here.
class Measurement(models.Model):
    date = models.DateTimeField(null=False)
    temperature = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    humidity = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    
    def __str__(self):
        return str(self.humidity)
        

    def get_temperature(self):
        return (self.date, self.temperature)
        
    def get_temperature(self):
        return (self.date, self.humidity)
        
    class Meta: 
        ordering = ['date']