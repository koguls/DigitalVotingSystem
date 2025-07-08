from django import forms
from .models import *
# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser



class CanditateForm(forms.ModelForm):
    
    class Meta:
        
        model = Candidate
        fields = ['name', 'party', 'symbol']
        
        widgets = {
            'name' : forms.TextInput(attrs={'class' : "form-control"}),
            'party' : forms.TextInput(attrs={'class' : "form-control"}),
            'symbol' : forms.FileInput(attrs={'class' : "form-control"})
        }
        
         

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'age', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter age'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        }
        
        

class ElectionForm(forms.ModelForm):
    class Meta:
        model = ElectionMention
        fields = ['name', 'start_time', 'end_time', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


# from django import forms
# from .models import Election

# class ElectionForm(forms.ModelForm):
#     class Meta:
#         model = Election
#         fields = ['name', 'start_time', 'end_time', 'is_active']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
#             'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
#             'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         }

        
    