from django import forms
from . import models

class RegisterForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "email", "password"]

    # Additional password field for confirmation
    conf_password = forms.CharField(max_length=128)

    widgets = {
        "password": forms.PasswordInput(),
        "conf_password": forms.PasswordInput()
    }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data["password"]
        conf_password = cleaned_data["conf_password"]

        if password != conf_password:
            raise forms.ValidationError("The passwords don't match.")


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=128)


class VendorRegisterForm(forms.ModelForm):
    class Meta:
        model = models.Vendor
        fields = ["name", "email", "address", "password"]

    # Additional password field for confirmation
    conf_password = forms.CharField(max_length=128)

    widgets = {
        "password": forms.PasswordInput(),
        "conf_password": forms.PasswordInput()
    }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data["password"]
        conf_password = cleaned_data["conf_password"]

        if password != conf_password:
            raise forms.ValidationError("The passwords don't match.")


class VendorLoginForm(LoginForm):
    pass