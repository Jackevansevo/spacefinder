from django import forms
from .models import Student, Department
from django.contrib.auth.models import User


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

    def clean(self, *args, **kwargs):
        self.clean_password()
        return super(UserForm, self).clean(*args, **kwargs)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('avatar', 'department')

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department"
    )

    def clean_avatar(self):
        """If user doesn't upload an avatar image then provide a default"""
        if self.data['avatar']:
            return self.data['avatar']
        return 'user_avatars/default.png'

    def clean(self, *args, **kwargs):
        self.clean_avatar()
        return super(StudentForm, self).clean(*args, **kwargs)


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)

    password = forms.CharField(widget=forms.PasswordInput())
