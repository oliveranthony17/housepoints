from django import forms
from django.forms import ModelForm
from .models import House, Student

class CreateStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'school_year', 'house']

class AwardPointsForm(ModelForm):
    class Meta:
        model = Student
        fields = ['points']

class CreateHouseForm(ModelForm):
    class Meta:
        model = House
        fields = '__all__'

# can do another form here
