from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'file', 'user', 'classroom')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PostForm, self).__init__(*args, **kwargs)

        self.fields['text'].widget.attrs={
            'class': 'textarea',
            'placeholder': 'Announce something to your class',
            'id': 'announce_textarea',
            'style': 'height: 10rem;',
        }
        self.fields['file'].widget.attrs={
            'class': 'd-none',
            'id': 'announce_add_attachment',
        }
        self.fields['user'].widget.attrs={
            'class': 'd-none',
        }
        self.fields['classroom'].widget.attrs={
            'class': 'd-none',
        }