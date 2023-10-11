from django.forms import ModelForm
from .models import Post
from django import forms

# Создаём модельную форму
class PostForm(ModelForm):
# В класс мета, как обычно, надо написать модель, по которой будет строиться форма, и нужные нам поля. Мы уже делали что-то похожее с фильтрами
   class Meta:
       model = Post
       fields = ['author', 'type', 'title', 'articleText', 'description']
       widgets = {
         'author' : forms.Select(attrs={
           'class': 'form-control',
         }),
         'title' : forms.TextInput(attrs={
           'class': 'form-control',
           'placeholder': 'Enter Title post'
         }),
         'type' : forms.Select(attrs={
           'class': 'form-control',
         }),
         'description' : forms.Textarea(attrs={
           'class': 'form-control',
         }),
         'articleText': forms.Textarea(attrs={
            'class': 'form-control',
         }),
       }