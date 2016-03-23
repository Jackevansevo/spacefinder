from .models import Student
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirm Password"
    )

    def clean_password(self):
        """Checks if the two passwords entered by the user are the same"""
        if self.data['password'] != self.data['confirm_password']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password']

    def clean(self, *args, **kwargs):
        self.clean_password()
        return super(UserForm, self).clean(*args, **kwargs)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('department', 'avatar')


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "Username",
            "class": "form-control"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder": "Password",
            "class": "form-control"
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'password')
