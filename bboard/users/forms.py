from django import forms
from django.core.exceptions import ValidationError
import re

class RegistrationForm(forms.Form):
    full_name = forms.CharField(
        label='ФИО',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    username = forms.CharField(
        label='Логин',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password_confirm = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных',
    )

    def clean_full_name(self):
        data = self.cleaned_data['full_name']
        if not re.match(r'^[А-Яа-яЁё\s-]+$', data):
            raise ValidationError('Только кириллица')

        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        if not re.match(r'^[A-Za-z]+$', data):
            raise ValidationError('Только латинница')
        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            self.add_error('password_confirm', 'Пароли не совпадают')