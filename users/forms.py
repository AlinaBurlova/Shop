from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class UserRegistrationForm(forms.ModelForm):

    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cleaned_data['password2']

    class Meta:
        model = User
        fields = ('username', 'password',
                  'first_name', 'last_name', 'email',
                  'phone', 'city', 'image')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',
                  'first_name', 'last_name', 'email',
                  'phone', 'city', 'image']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Старый пароль')
    new_password = forms.CharField(widget=forms.PasswordInput, label='Новый пароль')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Подтверждение нового пароля')

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        # Проверка на совпадение нового пароля со старым
        if old_password == new_password:
            self.add_error('new_password', 'Новый пароль не должен совпадать со старым.')

        # Проверка на совпадение нового пароля с подтверждением
        if new_password != confirm_password:
            self.add_error('confirm_password', 'Пароли не совпадают.')

        return cleaned_data