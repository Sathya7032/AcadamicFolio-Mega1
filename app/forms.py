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

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data   

    
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
