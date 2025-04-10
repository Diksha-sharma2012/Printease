from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserModel

from django import forms
from django.contrib.auth.hashers import make_password, check_password
from .models import UserModel

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserModel
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password1'])  # hash the password
        if commit:
            user.save()
        return user




class CustomLoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        print(email,password)
        # Get user by email
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise forms.ValidationError("No account found with this email.")

        if not check_password(password, user.password):
            raise forms.ValidationError("Incorrect password.")

        self.user = user

        # Authenticate user using username
        # user =  user.email, password=password)

        if user is None:
            raise forms.ValidationError("Invalid email or password.")

        return self.cleaned_data

    def get_user(self):
        return self.user