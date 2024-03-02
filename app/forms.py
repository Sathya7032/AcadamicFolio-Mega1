from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from multiupload.fields import MultiFileField
from tinymce.widgets import TinyMCE


class UserRegisterForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
		"class":"input",
		"type":"text",
		"placeholder":"Enter your username"
	}) ,label="UserName")

    email = forms.EmailField(widget=forms.TextInput(attrs={
		"class":"input",
		"type":"text",
		"placeholder":"Enter your email"
	}), label="Email")

    password1 = forms.CharField(widget=forms.TextInput(attrs={
		"class":"input",
		"type":"password",
		"placeholder":"Enter your password"
	}), label="Password")

    password2 = forms.CharField(widget=forms.TextInput(attrs={
		"class":"input",
		"type":"password",
		"placeholder":"Retype your password"
	}), label="Password")

    class Meta:
        model = User
        fields = ['email','username','password1','password2']

    
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ['title','content']	   

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class MemeForm(forms.ModelForm):

    class Meta:
        model = Meme
        fields = ['description','images']
