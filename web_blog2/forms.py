# forms.py
from django import forms
from .models import Comments, Contact

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['name', 'text']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'contact_number', 'email_id', 'body']


class UserInputForm(forms.Form):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('Hindi','Hindi'),
        ('Chinese','Chinese'),
        ('German','German'),
        ('Tamil','Tamil')
        # Add more choices as needed
    ]
    choices = forms.ChoiceField(choices=LANGUAGE_CHOICES, label='Select language')
    language = forms.CharField(max_length=100, label='Type the text to translate')

class UserBook(forms.Form):
    books = forms.CharField(
        max_length=200,
        label='Query',
        widget=forms.TextInput(attrs={'style': 'width: 700px; padding: 14px 10px;border-radius: 10px;'}),
    )

