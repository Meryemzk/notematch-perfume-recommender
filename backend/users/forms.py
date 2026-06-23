from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NoteMatchSignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        help_text="This name will be shown on your NoteMatch account.",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your username"}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Create a password"}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Repeat your password"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
        return user
