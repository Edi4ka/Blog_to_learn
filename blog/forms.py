from django import forms
from .models import Comment, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class AddComment(forms.ModelForm):
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': '50', 'rows': '10'}))

    class Meta:
        model = Comment
        fields = ('text', )

    def __init__(self, *args, **kwargs):
        super(AddComment, self).__init__(*args, **kwargs)
        self.text = None

    def clean(self):
        text = self.cleaned_data.get('text')
        if text:
            if len(text) < 5:
                raise forms.ValidationError('Сообщение слишком короткое')
        else:
            raise forms.ValidationError("Введите текст")
        self.text = text
        return self.cleaned_data


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')
    username = forms.CharField(required=True, max_length=20)
    password1 = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("The two password fields did not match.")
        return password2


class LoginUser(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', )

    def __init__(self, *args, **kwargs):
        self.user = None
        super(LoginUser, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError('Неправильное имя пользователя/пароль')
        return self.cleaned_data


class AddPost(forms.ModelForm):
    title = forms.CharField(required=True, max_length=200)
    text = forms.Textarea()
    tags = forms.SlugField()

    class Meta:
        model = Post
        fields = ('title', 'text',)

    def __init__(self, *args, **kwargs):
        super(AddPost, self).__init__(*args, **kwargs)
        self.text = None
        self.title = None
        self.tags = None

    def clean(self):
        title = self.cleaned_data.get('title')
        text = self.cleaned_data.get('text')
        tags = self.cleaned_data.get('tags')
        if len(text) < 5 or len(title) < 5:
            raise forms.ValidationError('Слишком короткий пост/заголовок')
        self.text = text
        self.title = title
        self.tags = tags
        return self.cleaned_data
