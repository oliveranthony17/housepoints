from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import House, Student

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        # default only requires username and password

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CreateHouseForm(ModelForm):
    class Meta:
        model = House
        fields = ['name', 'logo_url']

class CreateStudentForm(ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super(CreateStudentForm, self).__init__(*args, **kwargs)
        self.fields['house'].queryset = House.objects.filter(user=user)

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'school_year', 'house', 'points']
        labels = {'house': 'Choose House', 'points': 'Total points'}

class AwardPointsForm(ModelForm):

    class Meta:
        model = Student
        fields = ['points']
