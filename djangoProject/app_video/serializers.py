from rest_framework import serializers
from .models import Sentence,Word

class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields =  ['sentence_eg','sentence_kr', 'save_date']

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields =['word_eg','word_kr','save_date']