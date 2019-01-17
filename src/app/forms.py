from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )



    # def save(self, commit=True):
    #     user = super(SignUpForm, self).save(commit=False)
    #     first_name, last_name = self.cleaned_data["fullname"].split()
    #     user.first_name = first_name
    #     user.last_name = last_name
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
    #     return user


class NewPassword(forms.Form):
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        }
    ))
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Re-Enter Password'
        }
    ))





class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length = 100)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')