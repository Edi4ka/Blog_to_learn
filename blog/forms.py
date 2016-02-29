from django import forms
from .models import Comment


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
