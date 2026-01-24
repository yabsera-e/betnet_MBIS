from django import forms
from .models import Ads

class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ['company_name','fee','url','position','duration']

        widgets = {
            'company_name': forms.TextInput(attrs={
            'placeholder': 'ABC',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
            }),
            'fee': forms.TextInput(attrs={
            'placeholder': 'Kebede',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
            }),
            'url': forms.TextInput(attrs={
            'placeholder': 'http://www...',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
            }),
            # 'position': forms.ChoiceField(attrs={
            # 'placeholder': 'main',
            # 'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
            # # }),
            # 'duration': forms.IntegerField(attrs={
            # 'placeholder': 'duration(days)',
            # 'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 ',
            # }),
        }