# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, to_field='user_id', blank=True, null=True)
    video = models.ForeignKey('Video', models.DO_NOTHING, blank=True, null=True)
    quiz_date = models.DateTimeField(blank=True, null=True)
    answer_per = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quiz'


class Sentence(models.Model):
    sentence_id = models.AutoField(primary_key=True)
    video = models.ForeignKey('Video', models.DO_NOTHING, blank=True, null=True)
    sentence_eg = models.CharField(max_length=500, blank=True, null=True)
    sentence_kr = models.CharField(max_length=500, blank=True, null=True)
    save_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sentence'


class SentenceQuiz(models.Model):
    sentence_quiz_id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, models.DO_NOTHING, blank=True, null=True)
    quiz_0 = models.JSONField(db_column='quiz', blank=True, null=True)  # Field renamed because of name conflict.       
    is_wrong = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sentence_quiz'


class Test(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'


class Users(models.Model):
    user_id = models.CharField(unique=True, max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    passwd = models.CharField(max_length=50, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Video(models.Model):
    video_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, to_field='user_id', blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    save_date = models.DateTimeField(blank=True, null=True)
    view_count = models.IntegerField(blank=True, null=True)
    img = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video'


class Word(models.Model):
    word_id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video, models.DO_NOTHING, blank=True, null=True)
    word_eg = models.CharField(max_length=500, blank=True, null=True)
    word_kr = models.CharField(max_length=500, blank=True, null=True)
    save_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word'


class WordQuiz(models.Model):
    word_quiz_id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, models.DO_NOTHING, blank=True, null=True)
    quiz_0 = models.JSONField(db_column='quiz', blank=True, null=True)  # Field renamed because of name conflict.       
    is_wrong = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word_quiz'
