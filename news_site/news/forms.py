from django import forms
from .models import News, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from captcha.fields import CaptchaField

class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


#Описание связанной с моделью News формы
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'photo', 'is_published', 'category']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('context',)

class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема', widget=forms.TextInput())
    content = forms.CharField(label='Текст письма', widget=forms.Textarea(attrs={'rows': 5}))
    captcha = CaptchaField()