from django.db import models

# Create your models here.
class Location(models.Model):
    area = models.CharField(max_length=200)

    def __str__(self):
        return self.area

class Property(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    price = models.IntegerField()