from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


def _style(field, placeholder=""):
    field.widget.attrs.update({"class": "field", "placeholder": placeholder})


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
        field_classes = {"email": forms.EmailField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style(self.fields["email"], "you@example.com")
        _style(self.fields["password1"])
        _style(self.fields["password2"])


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Email"
        _style(self.fields["username"], "you@example.com")
        _style(self.fields["password"])
