from django.db import models
from django.contrib.auth.models import *


# Create your models here.

class House(models.Model):
  name = models.CharField(max_length=100, default="Gryffindor")
  logo_url = models.CharField(max_length=255, default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqLKGMXNr62iTZjs8oGIOSwOacxjcEP7y8uDNAw8E&s")

  user = models.ForeignKey(User, unique=False, on_delete=models.DO_NOTHING)

  def __str__(self):
    return self.name

class Student(models.Model):
  first_name = models.CharField(max_length=100, default="Harry")
  last_name = models.CharField(max_length=100, default="Potter")
  school_year = models.CharField(max_length=100, default="Kindergarten")

  points = models.IntegerField(default=0)
  user = models.ForeignKey(User, unique=False, on_delete=models.DO_NOTHING)

  house = models.ForeignKey(
    House,
    on_delete=models.DO_NOTHING,
    related_name="students",
    related_query_name="student"
  ) # students are NOT deleted if parent House is

  def __str__(self):
    return "%s %s - %s - %s" % (self.first_name, self.last_name, self.school_year, self.house.name)
