# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    quiz_date = models.DateTimeField(blank=True, null=True)
    answer_per = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, to_field='user_id', blank=True, null=True)
    video = models.ForeignKey('Video', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quiz'


class Sentence(models.Model):
    sentence_id = models.AutoField(primary_key=True)
    sentence_eg = models.CharField(max_length=500, blank=True, null=True)
    sentence_kr = models.CharField(max_length=500, blank=True, null=True)
    save_date = models.DateTimeField(blank=True, null=True)
    video = models.ForeignKey('Video', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sentence'


class SentenceQuiz(models.Model):
    sentence_quiz_id = models.AutoField(primary_key=True)
    quiz = models.JSONField(blank=True, null=True)
    is_wrong = models.IntegerField(blank=True, null=True)
    quiz_id = models.ForeignKey(Quiz, models.DO_NOTHING, db_column='quiz_id', blank=True, null=True)  # Field renamed because of name conflict.

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
    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(unique=True, max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    passwd = models.CharField(max_length=50, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Video(models.Model):
    video_id = models.AutoField(primary_key=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    save_date = models.DateTimeField(blank=True, null=True)
    view_count = models.IntegerField(blank=True, null=True)
    img = models.TextField(blank=True, null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, to_field='user_id', blank=True, null=True)
    script = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video'


class Word(models.Model):
    word_id = models.AutoField(primary_key=True)
    word_eg = models.CharField(max_length=500, blank=True, null=True)
    word_kr = models.CharField(max_length=500, blank=True, null=True)
    save_date = models.DateTimeField(blank=True, null=True)
    video = models.ForeignKey(Video, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word'


class WordQuiz(models.Model):
    word_quiz_id = models.AutoField(primary_key=True)
    quiz = models.JSONField(blank=True, null=True)
    is_wrong = models.IntegerField(blank=True, null=True)
    quiz_id = models.ForeignKey(Quiz, models.DO_NOTHING, db_column='quiz_id', blank=True, null=True)  # Field renamed because of name conflict.

    class Meta:
        managed = False
        db_table = 'word_quiz'
