from django import forms

from app.models import Comment


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, label='')
