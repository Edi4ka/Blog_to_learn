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

    def __init__(self, *args, **kwargs):
        super(AddComment, self).__init__(*args, **kwargs)
        self.text = None

    def clean(self):
        text = self.cleaned_data.get('text')
        if text:
            if len(text) < 5:
                raise ValidationError('Сообщение слишком короткое')
        else:
            raise ValidationError("Введите текст")
        self.text = text
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
    title = forms.CharField()
    text = forms.Textarea()
    tags = forms.SlugField()

    class Meta:
        model = Post
        fields = ('title', 'text',)

    def __init__(self, *args, **kwargs):
        super(AddPost, self).__init__(*args, **kwargs)
        self.text_ = None
        self.title_ = None
        self.tags_ = None

    def clean(self):
        title = self.cleaned_data.get('title')
        text = self.cleaned_data.get('text')
        tags = self.cleaned_data.get('tags')
        if text is None:
            raise ValidationError('Введите текст')
        if title is None:
            raise ValidationError('Введите заголовок')
        elif len(title) < 5 or len(text) < 5:
            raise ValidationError('Текст/заголовок слишком короткие')
        self.text_ = text
        self.title_ = title
        if tags is None:
            self.tags_ = ''
        elif tags is not None:
            self.tags = tags
        return self.cleaned_data


class EditComment(forms.ModelForm):
    text = forms.TextInput()

    class Meta:
        model = Comment
        fields = ('text', )

    def __init__(self, *args, **kwargs):
        super(EditComment, self).__init__(*args, **kwargs)
        self.text_ = None

    def clean(self):
        text = self.cleaned_data.get('text')
        self.text_ = text
        return self.cleaned_data
