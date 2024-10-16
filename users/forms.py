from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class UserRegistrationForm(forms.ModelForm):

    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cleaned_data['password2']

    class Meta:
        model = User
        fields = ('username', 'password',
                  'first_name', 'last_name', 'email',
                  'phone', 'city')


class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput)
    new_password_1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    new_password_2 = forms.CharField(label="Повторите новый пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data["old_password"]
        new_password_1 = cleaned_data["new_password_1"]
        new_password_2 = cleaned_data["new_password_2"]

        if new_password_1 and new_password_2 and new_password_1 != new_password_2:
            raise forms.ValidationError('Пароли не совпадают!')

        if new_password_1 and new_password_2 and new_password_1 == new_password_2 and old_password == new_password_1:
            raise forms.ValidationError('Пароль совпадает с текущим!')

        return cleaned_data
