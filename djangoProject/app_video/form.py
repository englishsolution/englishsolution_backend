from django import forms
from .models import Sentence,Word

class SentenceForm(forms.ModelForm):
    class Meta:
        model = Sentence
        fields = ['video', 'sentence_eg', 'sentence_kr', 'save_date']

class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['video', 'word_eg', 'word_kr', 'save_date']