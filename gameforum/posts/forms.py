from django import forms
from .models import Post, Tag

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Post
        fields = ('title', 'category', 'content', 'image', 'tags')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }