from django import forms
from .models import Student, Department
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {'password': forms.PasswordInput()}

    # Add an extra password confirmation field
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        """Checks if the two passwords entered by the user are the same"""
        if self.data['password'] != self.data['confirm_password']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('avatar', 'department')

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department"
    )

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if avatar:
            # Ensure the image is no larger than 2MB
            if avatar._size > 2*1024*1024:
                raise forms.ValidationError("Image file too large ( > 4mb )")
            return avatar
        else:
            raise forms.ValidationError("Couldn't read uploaded image")
        return avatar


class LoginForm(forms.Form):
    """Allows the student to login with username and password combination"""
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Wrong username or password")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
