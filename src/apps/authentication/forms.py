from django import forms

from .models import User


class CustomUserCreateForm(forms.ModelForm):
    """Form for creating a new custom user"""

    class Meta:
        model = User
        fields = ("username", "email", "password")


class CustomUserChangeForm(forms.ModelForm):
    """Form for changing a user data"""

    class Meta:
        model = User
        fields = ("username", "email")
