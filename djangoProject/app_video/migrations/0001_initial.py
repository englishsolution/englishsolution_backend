# Generated by Django 5.0.6 on 2024-08-19 19:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('quiz_id', models.AutoField(primary_key=True, serialize=False)),
                ('quiz_date', models.DateTimeField(auto_now_add=True)),
                ('answer_per', models.DecimalField(decimal_places=2, max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'quiz',
            },
        ),
        migrations.CreateModel(
            name='SentenceQuiz',
            fields=[
                ('sentence_quiz_id', models.AutoField(primary_key=True, serialize=False)),
                ('quiz', models.JSONField()),
                ('is_wrong', models.IntegerField()),
                ('quiz_0', models.ForeignKey(db_column='quiz_id', on_delete=django.db.models.deletion.CASCADE, to='app_video.quiz')),
            ],
            options={
                'db_table': 'sentence_quiz',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('video_id', models.AutoField(primary_key=True, serialize=False)),
                ('link', models.CharField(max_length=500)),
                ('title', models.CharField(max_length=50)),
                ('save_date', models.DateTimeField(auto_now_add=True)),
                ('view_count', models.IntegerField()),
                ('img', models.TextField()),
                ('script', models.TextField(default='default_script')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'video',
            },
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('sentence_id', models.AutoField(primary_key=True, serialize=False)),
                ('sentence_eg', models.CharField(max_length=500)),
                ('sentence_kr', models.CharField(max_length=500)),
                ('save_date', models.DateTimeField(auto_now_add=True)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_video.video')),
            ],
            options={
                'db_table': 'sentence',
            },
        ),
        migrations.AddField(
            model_name='quiz',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_video.video'),
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('word_id', models.AutoField(primary_key=True, serialize=False)),
                ('word_eg', models.CharField(max_length=500)),
                ('word_kr', models.CharField(max_length=500)),
                ('save_date', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(max_length=500)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_video.video')),
            ],
            options={
                'db_table': 'word',
            },
        ),
        migrations.CreateModel(
            name='WordQuiz',
            fields=[
                ('word_quiz_id', models.AutoField(primary_key=True, serialize=False)),
                ('quiz', models.JSONField()),
                ('is_wrong', models.IntegerField()),
                ('quiz_0', models.ForeignKey(db_column='quiz_id', on_delete=django.db.models.deletion.CASCADE, to='app_video.quiz')),
            ],
            options={
                'db_table': 'word_quiz',
            },
        ),
    ]
