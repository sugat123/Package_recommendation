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


    def clean(self):
        print("here in clean")
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            print('raised rairased')
            raise forms.ValidationError("Password do not match. Please re-type your password. !!")
        else:
            return self.cleaned_data


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length = 100)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')



class FilterForm(forms.Form):
    name = forms.CharField(max_length=50)
    duration = forms.CharField(max_length=50)
    location = forms.CharField(max_length=50)




class SearchForm(forms.Form):
    search = forms.CharField(max_length=50)