from .models import Student
from django.contrib.auth.models import User
from django import forms
from .models import Department


class UserForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Username", "class": "form-control"}
    ))

    email = forms.EmailField(widget=forms.TextInput(
        attrs={"placeholder": "Email", "class": "form-control"}
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Password", "class": "form-control"}
    ))

    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Confirm Password", "class": "form-control"}
    ))

    def clean_password(self):
        """Checks if the two passwords entered by the user are the same"""
        if self.data['password'] != self.data['confirm_password']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password']

    def clean(self, *args, **kwargs):
        self.clean_password()
        return super(UserForm, self).clean(*args, **kwargs)


class StudentForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        empty_label="Select Department",
        queryset=Department.objects.all(), widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        ))
    avatar = forms.ImageField(required=False)


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Username", "class": "form-control"}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Password", "class": "form-control"}
    ))
