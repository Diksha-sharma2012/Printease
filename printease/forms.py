from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]       # Use email as username
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user



class CustomLoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        # Get user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("No account found with this email.")

        # Authenticate user using username
        user = authenticate(username=user.username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid email or password.")

        self.user = user
        return self.cleaned_data

    def get_user(self):
        return self.user