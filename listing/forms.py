from django import forms
from .models import Listing, ListingMedia, City, SubCity


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title','desc','price','rooms','bedrooms','bathrooms','square_metre','city','sub_city','area','amenities','phone_number1','phone_number2']
        
        widgets = {
            'title': forms.TextInput(attrs={
            'placeholder': 'Luxury Apartment',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-lime-500 focus:border-lime-500 block w-full p-2.5 ',
            }),
            'description': forms.Textarea(attrs={
            'placeholder': 'write description',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-lime-500 focus:border-lime-500 block w-full p-2.5 ',
            }),
            'price': forms.TextInput(attrs={
            'placeholder': '20000',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-lime-500 focus:border-lime-500 block w-full p-2.5 ',
            }),
            'rooms': forms.TextInput(attrs={
            'placeholder': '4',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-lime-500 focus:border-lime-500 block w-full p-2.5 ',
            }),
            'bedrooms': forms.TextInput(attrs={
            'placeholder': '2',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-lime-500 focus:border-lime-500 block w-full p-2.5 ',
            }),
            'bathrooms': forms.TextInput(attrs={
            'placeholder': '1',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-lime-500 focus:border-lime-500 block w-full p-2.5 ',
            }),
            'square_metre': forms.TextInput(attrs={
            'placeholder': '145',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-lime-500 focus:border-lime-500 block w-full p-2.5 ',
            }),
            'city': forms.Select(attrs={
            'placeholder': 'Addis Ababa',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-lime-500 focus:border-lime-500 block w-full p-2.5 ',
            }),
            'sub_city': forms.Select(attrs={
            'placeholder': 'Kirkos',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-lime-500 focus:border-lime-500 block w-full p-2.5 ',
            }),
            'area': forms.TextInput(attrs={
            'placeholder': 'Kazanchis',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-lime-500 focus:border-lime-500 block w-full p-2.5 ',
            }),
            'phone_number1': forms.TextInput(attrs={
            'placeholder': '091234___',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-lime-500 focus:border-lime-500 block w-full p-2.5 ',
            }),
            'phone_number2': forms.TextInput(attrs={
            'placeholder': '094321___',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-lime-500 focus:border-lime-500 block w-full p-2.5 ',
            }),
            'amenities': forms.CheckboxSelectMultiple(attrs={
                'class': 'custom-checkbox'
            }),
        }

class CitySelectForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Select a city")

class SubCitySelectForm(forms.Form):
    sub_city = forms.ModelChoiceField(queryset=SubCity.objects.none())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_city'].queryset = SubCity.objects.filter(city_id=self.initial.get('city'))