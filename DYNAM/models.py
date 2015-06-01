from django.db import models
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))




class Detail(models.Model):
    producer = models.CharField(max_length=65)

class Car(models.Model):
   title = models.TextField()
   release = models.DateField()
   engine_v  = models.FloatField()
   german = models.BooleanField()
   details = models.ManyToManyField(Detail,related_name="car_details")
   category = models.ForeignKey('Category',db_column='category_idcategory', related_name='cars')

class Category(models.Model):
    name = models.TextField()