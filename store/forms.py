from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from store.models import Comment,Cart


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']



class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('subject', 'comment', 'rate')


class CartForm(forms.ModelForm):
    
    class Meta:
        model = Cart
        fields = ['quantity']
