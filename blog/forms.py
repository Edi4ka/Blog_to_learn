from django import forms
from django.forms import ValidationError
from .models import Comment, Post, NewUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


class AddComment(forms.ModelForm):
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': '50', 'rows': '10'}))

    class Meta:
        model = Comment
        fields = ('text', )

    def clean(self):
        text = self.cleaned_data.get('text')
        if text:
            if len(text) < 5:
                raise ValidationError('Сообщение слишком короткое')
        else:
            raise ValidationError("Введите текст")
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=25)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(max_length=255)

    class Meta:
        model = NewUser
        fields = ('username', 'password1', 'password2', 'email')

    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password2 != password1:
            raise ValidationError('Пароли не совпадают')
        elif len(password1) < 5:
            raise ValidationError('Пароль слишком короткий')
        elif len(username) < 3:
            raise ValidationError('Никнейм слишком короткий')
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class LoginUser(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = NewUser
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
                raise ValidationError('Неправильное имя пользователя/пароль')
        return self.cleaned_data


class AddPost(forms.ModelForm):
    title = forms.TextInput()
    text = forms.TextInput()
    tags = forms.SlugField()

    class Meta:
        model = Post
        fields = ('title', 'text', 'tags', )

    def clean(self):
        title = self.cleaned_data.get('title')
        text = self.cleaned_data.get('text')
        tags = self.cleaned_data.get('tags')
        if len(title) < 5:
            raise ValidationError('Заголовок слишком короткий')
        if len(text) < 20:
            raise ValidationError('Текст слишком короткий')
        if len(tags) < 5:
            raise ValidationError('Тэг слишком короткий')
        return self.cleaned_data


class EditComment(forms.ModelForm):
    text = forms.TextInput()

    class Meta:
        model = Comment
        fields = ('text', )

    def __init__(self, *args, **kwargs):
        super(EditComment, self).__init__(*args, **kwargs)
        self.text_to_view = None

    def clean(self):
        text = self.cleaned_data.get('text')
        if len(text) < 5:
            raise ValidationError('Сообщение слишком короткое')
        self.text_to_view = text
        return self.cleaned_data


class EditPost(forms.ModelForm):
    text = forms.TextInput()
    title = forms.TextInput()

    class Meta:
        model = Post
        fields = ('text', 'title', )

    def __init__(self, *args, **kwargs):
        super(EditPost, self).__init__(*args, **kwargs)
        self.text_to_view = None
        self.title_to_view = None

    def clean(self):
        text = self.cleaned_data.get('text')
        title = self.cleaned_data.get('title')
        if len(text) < 10:
            raise ValidationError('Сообщение слишком короткое')
        if len(title) < 5:
            raise ValidationError('Заголовок слишком короткий')
        self.text_to_view = text
        self.title_to_view = title
        return self.cleaned_data
