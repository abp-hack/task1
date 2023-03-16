from django import forms
from .models import Student
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError




class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('name', 'surname', 'mindame', 'email', 'gender', 'password')
        widgets = {
            'email': forms.TextInput(attrs={'data-mask': '000000'})
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if len(User.objects.filter(username=email)):
            raise ValidationError('Пользователь с таким email уже существует')
        return email