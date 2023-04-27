from django.db import models
from django.forms import fields
from .models import UploadImage
from django import forms
from django.forms.widgets import ClearableFileInput




class UserImage(forms.ModelForm):
    class Meta:
        # To specify the model to be used to create form
        model = UploadImage
        # It includes all the fields of model
        fields = ('image',)
        widgets = {
            'image': ClearableFileInput(attrs={'class': 'border border-2 border-dark border-end-0 rounded-start', 'accept': 'image/*'})
        }


