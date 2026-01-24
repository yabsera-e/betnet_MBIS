from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    widgets = {
            'content': forms.TextInput(attrs={
            'placeholder': 'write your comment...',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-[25rem] p-2.5 ',
            }),
        }