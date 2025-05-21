from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('recipient', 'subject', 'content')
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Тема'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Сообщение...'}),
        }
