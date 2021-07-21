from django.db import models

# Create your models here.


class Car(models.Model):
    car_name = models.CharField(max_length=200)
    car_model = models.CharField(max_length=200)
    engine_no = models.IntegerField()

    def __str__(self):
        return self.car_name

