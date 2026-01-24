from django import forms
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','password']

        widgets = {
            'first_name': forms.TextInput(attrs={
            'placeholder': 'Abebe',
            'class': 'p-6 rounded bg-gray-50 border border-gray-100 text-gray-900  rounded-lg focus:ring-amber-500 focus:border-amber-500 block w-full p-2.5 ',
            }),
            'last_name': forms.TextInput(attrs={
            'placeholder': 'Kebede',
            'class': 'p-6 rounded bg-gray-50 border border-gray-100 text-gray-900 rounded-lg focus:ring-amber-500 focus:border-amber-500 block w-full p-2.5 ',
            }),
            'email': forms.TextInput(attrs={
            'placeholder': 'abekebe@example.com',
            'class': 'p-6 rounded bg-gray-50 border border-gray-100 text-gray-900 rounded-lg focus:ring-amber-500 focus:border-amber-500 block w-full p-2.5 ',
            }),
            'password': forms.PasswordInput(attrs={
            'placeholder': '********',
            'class': 'p-6 rounded bg-gray-50 border border-gray-100 text-gray-900 rounded-lg focus:ring-amber-500 focus:border-amber-500 block w-full p-2.5 ',
            }),
        }

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','password']
        widgets = {
            'email': forms.TextInput(attrs={
            'placeholder': 'abekebe@example.com',
            'class': 'p-6 rounded bg-gray-50 border border-gray-100 text-gray-900 rounded-lg focus:ring-amber-500 focus:border-amber-500 block w-full p-2.5 ',
            }),
            'password': forms.PasswordInput(attrs={
            'placeholder': '********',
            'class': 'p-6 rounded bg-gray-50 border border-gray-100 text-gray-900 rounded-lg focus:ring-amber-500 focus:border-amber-500 block w-full p-2.5 ',
            }),
        }



class ProfileUpdateForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'first name',
            'class': 'p-2 rounded bg-gray-50 border border-gray-100 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
        }),
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'last name',
            'class': 'p-2 rounded bg-gray-50 border border-gray-100 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
        }),
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'placeholder': 'email',
            'class': 'p-2 rounded bg-gray-50 border border-gray-100 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
        }),
    )
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '********',
            'class': 'p-2 rounded bg-gray-50 border border-gray-100 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
        }),
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '********',
            'class': 'p-2 rounded bg-gray-50 border border-gray-100 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
        }),
    )