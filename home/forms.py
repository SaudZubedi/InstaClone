from django import forms
from django.db.models import fields

from .models import Comment, Post, PostLike

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'content',
            'caption',
            'allow_comments'
        ]

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs = {'name': 'content'}
        self.fields['caption'].widget.attrs = {'class': 'caption', 'placeholder': '(optional)'}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields  = ['comment', ]


    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs = {'class': 'comment-form', 'placeholder': 'Add a comment...', 'autocorrect': 'off', 'autocomplete': 'off', 'aria-label': 'Add a comment...', 'id': 'comment-area'}

class EditComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', )

    def __init__(self, *args, **kwargs):
        super(EditComment, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs = {'class': 'edit-comment', 'id': 'edit-comment', 'placeholder': 'Edit comment...', 'name': 'edit-comment'}