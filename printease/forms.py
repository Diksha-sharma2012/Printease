from django.contrib.auth import get_user_model, authenticate
# from django.contrib.auth.forms import UserCreationForm
from django import forms
# from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User



class SignUpForm(forms.ModelForm):

    class Meta:  # <-- should be Meta, not Mets
        model = User
        fields = ['username', 'email', 'password']




class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        User = get_user_model()

        if email and password:
            try:
                user = User.objects.get(email=email)
                print(user.email)
                print(user.username)
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password.")

            # user = authenticate(username=user.username, password=password)
            print(user.username)
            if user is None:
                raise forms.ValidationError("Invalid email or password.")

            if not user.is_active:
                raise forms.ValidationError("This account is inactive.")

            self.user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)