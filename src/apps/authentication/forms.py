from django import forms

from .models import User


class CustomUserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password")


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")
