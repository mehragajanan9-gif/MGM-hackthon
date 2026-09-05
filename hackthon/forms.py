from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Complaint, Profile


# ==========================
# REGISTER FORM
# ==========================

class RegisterForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter username"
            }
        )
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email"
            }
        )
    )

    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter phone number"
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter password"
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm password"
            }
        )
    )

    class Meta:

        model = User

        fields = [
            "username",
            "email",
            "phone",
            "password1",
            "password2",
        ]

    def clean_email(self):

        email = self.cleaned_data["email"].strip()

        if User.objects.filter(
            email__iexact=email
        ).exists():

            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def save(self, commit=True):

        user = super().save(commit=False)

        user.email = self.cleaned_data["email"]

        if commit:

            user.save()

            Profile.objects.get_or_create(
                user=user,
                defaults={
                    "phone": self.cleaned_data.get("phone", ""),
                    "role": "citizen"
                }
            )

        return user


# ==========================
# COMPLAINT FORM
# ==========================

class ComplaintForm(forms.ModelForm):

    class Meta:

        model = Complaint

        fields = [
            "title",
            "description",
            "image",
            "location",
            "latitude",
            "longitude",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: Large pothole near college"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe the problem in detail..."
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Location will be detected automatically or enter manually"
                }
            ),

            "latitude": forms.HiddenInput(),

            "longitude": forms.HiddenInput(),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*"
                }
            ),
        }   