from django import forms
from .models import *
from django.forms import formset_factory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.forms import UserCreationForm

class_attendance = (
    ('Present','Present'),
    ('Absent','Absent'),
)
subject_choices=(('Maths','Maths'),('Science','Science'),('English','English'))
year_choices = (
        ('I','I'),
    ('II','II'),
    ('III','III'),
    ('IV','IV'),
    )
User = get_user_model()

class addStudentForm(forms.ModelForm):

    class Meta:
        model=Student
        fields=['name','standard','gender','mentor']

class AttendanceForm(forms.Form):
    has_attended=forms.ChoiceField(widget=forms.RadioSelect, choices=class_attendance)

class addVolounteerForm(forms.ModelForm):
    class Meta:
        model=Volounteer
        fields=['volounteer_name','volounteer_role','volounteer_year','volounteer_subject_taught']

class subjectForm(forms.ModelForm):
    class Meta:
        model=Date
        fields=['subject']

class registrationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    year=forms.ChoiceField(choices=year_choices)

    class Meta:
        model=User
        fields=['first_name','last_name','email','year','password1','password2']

    def save(self,commit=True):
        user=super(registrationForm,self).save(commit=False)
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.email=self.cleaned_data['email']
        user.username=user.first_name+' '+user.last_name
        
        if commit:
            user.save()
            v1=Volounteer()
            v1.volounteer_name=user.first_name+' '+user.last_name
            v1.volounteer_year=self.cleaned_data['year']
            v1.volounteer_role='Mentor'
            v1.save()
        
        return user