from .models import Student
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('department', 'avatar')
