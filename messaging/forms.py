from .models import Message
from django import forms

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

        widgets = {
            'content': forms.TextInput(attrs={
            'placeholder': 'Type your message...',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-lime-500 focus:border-lime-500 block w-full sm:w-[50%] p-2.5',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['autofocus'] = True