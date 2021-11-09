from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from app.models import ContactUser
from django import forms

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"


class ContactForm(ModelForm):
    class Meta:
        model = ContactUser
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w3-input w3-border my-3', 'placeholder': 'Name'}),
            'email_address': forms.EmailInput(attrs={'class': 'w3-input w3-border my-3', 'placeholder': 'Email'}),
            'subject': forms.TextInput(attrs={'class': 'w3-input w3-border my-3', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'w3-input w3-border my-3', 'placeholder': 'Message'}),
        }
        labels = {
            'name': '',
            'email_address': '',
            'subject': '',
            'message': ''
        }