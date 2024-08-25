from django.db import models
from django.conf import settings

# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=80)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group'
#
#
# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)
#
#
# class AuthPermission(models.Model):
#     name = models.CharField(max_length=50)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)
#
#
# class Auth_User(models.Model):  # USER 관리 모델
#     password = models.CharField(max_length=128, null=False)
#     last_login = models.DateTimeField(auto_now=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=30)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.CharField(max_length=75)
#     is_staff = models.IntegerField() #True이면 관리자 사이트 접근 가능
#     is_active = models.IntegerField() #계정 활성화
#     date_joined = models.DateTimeField(auto_now_add=True)
#     state = models.IntegerField() # 관리자(모든 권한)
#
#     class Meta:
#         db_table = 'auth_user'
#
#
# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(Auth_User, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)
#
#
# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(Auth_User, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)
#
#
# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(Auth_User, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'
#
#
# class DjangoContentType(models.Model):
#     name = models.CharField(max_length=100)
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)
#
#
# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_migrations'
#
#
# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_session'

class Profile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 기본 사용자 모델을 참조합니다
        on_delete=models.CASCADE,  # 사용자가 삭제될 때 이 프로필도 삭제됩니다
    )

    def __str__(self):
        return self.user.username

# 장고의 auth user로 대체
# class Users(models.Model):  #user
#     id = models.BigAutoField(primary_key=True)  #고유 아이디 index
#     user_id = models.CharField(unique=True, max_length=50)
#     email = models.CharField(max_length=50)
#     passwd = models.CharField(max_length=50)
#     #state = models.IntegerField()
#
#     class Meta:
#         db_table = 'users'

class Video(models.Model):
    video_id = models.AutoField(primary_key=True)
    link = models.CharField(max_length=500) #영상링크
    title = models.CharField(max_length=50) #영상제목
    save_date = models.DateTimeField(auto_now_add=True) #저장날짜
    view_count = models.IntegerField() #시청횟수
    img = models.TextField() #영상 썸네일
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 기본 사용자 모델을 참조합니다
        on_delete=models.CASCADE
    )
    script = models.TextField(default='default_script')
    video_identify = models.CharField(unique=True, max_length=45) #비디오 고유 id
    class Meta:
        db_table = 'video'

class Sentence(models.Model):
    sentence_id = models.AutoField(primary_key=True)
    sentence_eg = models.CharField(max_length=500)
    sentence_kr = models.CharField(max_length=500)
    save_date = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Video,on_delete=models.CASCADE)

    class Meta:
        db_table = 'sentence'

class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    quiz_date = models.DateTimeField(auto_now_add=True)
    answer_per = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 기본 사용자 모델을 참조합니다
        on_delete=models.CASCADE
    )
    video = models.ForeignKey(Video, models.CASCADE)

    class Meta:
        db_table = 'quiz'

class SentenceQuiz(models.Model):
    sentence_quiz_id = models.AutoField(primary_key=True)
    quiz = models.JSONField()  # { "Qustion" : "Answer" }
    is_wrong = models.IntegerField() # 0 : 맞음 , 1 : 틀림
    quiz_0 = models.ForeignKey(Quiz, models.CASCADE, db_column='quiz_id') # Field renamed because of name conflict.

    class Meta:
        db_table = 'sentence_quiz'



class Word(models.Model):
    word_id = models.AutoField(primary_key=True)
    word_eg = models.CharField(max_length=500)
    word_kr = models.CharField(max_length=500)
    save_date = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Video, models.CASCADE)
    type=models.CharField(max_length=500)

    class Meta:
        db_table = 'word'

class WordQuiz(models.Model):
    word_quiz_id = models.AutoField(primary_key=True)
    quiz = models.JSONField() # { "Qustion" : "Answer" }
    is_wrong = models.IntegerField() # 0 : 맞음 , 1 : 틀림
    quiz_0 = models.ForeignKey(Quiz, models.CASCADE, db_column='quiz_id')  # Field renamed because of name conflict.

    class Meta:# Field renamed because of name conflict.
        db_table = 'word_quiz'
