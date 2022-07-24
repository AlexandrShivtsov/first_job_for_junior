import uuid
from django.conf import settings
from django import forms
from accounts.models import User
from accounts.tasks import activate_mail
from django.urls import reverse


'''форма для регистрации пользователя'''


class SingUpForm(forms.ModelForm):

    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password1',
        )

    def clean(self):
        '''переопределям метод clean() и сравниваем password1 и password2, если они не совпадают
        вызываем исключене forms.ValidationError()'''
        cleaned_data = super().clean()
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data

    def save(self, commit=True):
        '''переопределям метод save(), изменяем поле is_active на False для последующе активации через
        ссылку по email, сохраняем пароль в db'''
        instance = super().save(commit=False)

        instance.is_active = False

        '''присваиваем username при помощи uuid.uuid4()'''
        instance.username = str(uuid.uuid4())

        '''присвоили пароль'''
        instance.set_password(self.cleaned_data['password1'])

        '''составили ссылку для активации'''
        activation_path = reverse("accounts:activate_user", args=[instance.username])

        '''отправили ссылку для активации'''
        activate_mail.delay(
            f'{settings.HTTP_SHCEMA}://{settings.DOMAIN}{activation_path}',
            instance.email
        )

        if commit:
            instance.save()
        return instance
