from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from regist.models import Profile

class RegForm(UserCreationForm):
    avatar = forms.ImageField(label='Аватарка', widget=forms.FileInput, required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")
        widgets = {'password'}

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.__class__ == forms.widgets.FileInput:
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control-file'
                else:
                    field.widget.attrs.update({'class': 'form-control-file'})
            else:
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs.update({'class': 'form-control'})


    def clean_username(self):
        username = self.cleaned_data['username']
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Данный логин уже занят")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Данный e-mail уже занят")
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        profile = Profile()
        profile.user = user
        profile.avatar = self.cleaned_data['avatar']
        profile.save()

        return profile

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=150,
                               widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Логин', 'class': 'form-control'}))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form-control'}))

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            if username and password:
                user = authenticate(username=username, password=password)
                if user is None:
                    raise forms.ValidationError('Неверный логин / пароль.')