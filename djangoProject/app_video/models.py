from django.db import models


class AppVideoProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'app_video_profile'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

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
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
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


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    quiz_date = models.DateTimeField()
    answer_per = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    video = models.ForeignKey('Video', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'quiz'


class Sentence(models.Model):
    sentence_id = models.AutoField(primary_key=True)
    sentence_eg = models.CharField(max_length=500)
    sentence_kr = models.CharField(max_length=500)
    save_date = models.DateTimeField()
    video = models.ForeignKey('Video', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sentence'


class SentenceQuiz(models.Model):
    sentence_quiz_id = models.AutoField(primary_key=True)
    quiz = models.JSONField()
    is_wrong = models.IntegerField()
    quiz_id = models.ForeignKey(Quiz, models.DO_NOTHING, db_column='quiz_id')  # Field renamed because of name conflict.

    class Meta:
        managed = False
        db_table = 'sentence_quiz'


class Video(models.Model):
    video_id = models.AutoField(primary_key=True)
    link = models.CharField(max_length=500)
    title = models.CharField(max_length=50)
    save_date = models.DateTimeField()
    img = models.TextField()
    script = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    video_identitfy = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'video'


class Word(models.Model):
    word_id = models.AutoField(primary_key=True)
    word_eg = models.CharField(max_length=500)
    word_kr = models.CharField(max_length=500)
    save_date = models.DateTimeField()
    type = models.CharField(max_length=500)
    video = models.ForeignKey(Video, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'word'


class WordQuiz(models.Model):
    word_quiz_id = models.AutoField(primary_key=True)
    quiz = models.JSONField()
    is_wrong = models.IntegerField()
    quiz_id = models.ForeignKey(Quiz, models.DO_NOTHING, db_column='quiz_id')  # Field renamed because of name conflict.

    class Meta:
        managed = False
        db_table = 'word_quiz'
