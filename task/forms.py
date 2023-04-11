from .models import Comment
from django import forms


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
