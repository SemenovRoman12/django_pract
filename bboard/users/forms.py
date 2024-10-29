from django import forms
from django.core.exceptions import ValidationError
from .models import User

class RegistrationForm(forms.ModelForm):
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
    avatar = forms.ImageField(
        label='Аватар',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )
    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных',
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        return username

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password != password_confirm:
            raise ValidationError("Пароли не совпадают.")
        return password_confirm

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > 3 * 1024 * 1024:
            raise ValidationError("Размер файла аватара не должен превышать 3 МБ.")
        return avatar

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'avatar', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 3 * 1024 * 1024:
                raise forms.ValidationError("Размер файла аватара не должен превышать 3 МБ.")
        return avatar




