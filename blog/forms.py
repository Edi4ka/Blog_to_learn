from django import forms
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
