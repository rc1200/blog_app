from django import forms
from .models import Post, Comment

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from tinymce import TinyMCE


# from crispy_forms.layout bootstrep import (
#     PrependedText, PrependedAppendedText, FormActions)

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = ('title', 'text', 'content')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class UserForm(forms.ModelForm):

    # utilizing the password widget so when you type, password is hidden
    password = forms.CharField(widget=forms.PasswordInput())
    helper = FormHelper()
    helper.form_method = 'POST'
    # the inputs you want to show for the
    helper.add_input(Submit('Sign up', 'Sign up', css_class='btn-primary'))
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    # class Meta:
    #     model = Comment
    #     fields = ('text',)