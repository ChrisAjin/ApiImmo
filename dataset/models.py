from django.db import models

class DataSet(models.Model):
    url = models.URLField(unique=True) 
    price = models.FloatField(null=True, blank=True)
    charges = models.FloatField(null=True, blank=True)
    department = models.CharField(max_length=10, null=True, blank=True)  # Corrigez l'attribut `department`
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.title or self.url