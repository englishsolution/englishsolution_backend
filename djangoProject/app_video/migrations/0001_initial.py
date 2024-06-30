# Generated by Django 5.0.6 on 2024-06-30 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('quiz_id', models.AutoField(primary_key=True, serialize=False)),
                ('quiz_date', models.DateTimeField(blank=True, null=True)),
                ('answer_per', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'db_table': 'quiz',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('sentence_id', models.AutoField(primary_key=True, serialize=False)),
                ('sentence_eg', models.CharField(blank=True, max_length=500, null=True)),
                ('sentence_kr', models.CharField(blank=True, max_length=500, null=True)),
                ('save_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sentence',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SentenceQuiz',
            fields=[
                ('sentence_quiz_id', models.AutoField(primary_key=True, serialize=False)),
                ('quiz_0', models.JSONField(blank=True, db_column='quiz', null=True)),
                ('is_wrong', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sentence_quiz',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'test',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('passwd', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('video_id', models.AutoField(primary_key=True, serialize=False)),
                ('link', models.CharField(blank=True, max_length=500, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('save_date', models.DateTimeField(blank=True, null=True)),
                ('view_count', models.IntegerField(blank=True, null=True)),
                ('img', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'video',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('word_id', models.AutoField(primary_key=True, serialize=False)),
                ('word_eg', models.CharField(blank=True, max_length=500, null=True)),
                ('word_kr', models.CharField(blank=True, max_length=500, null=True)),
                ('save_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'word',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WordQuiz',
            fields=[
                ('word_quiz_id', models.AutoField(primary_key=True, serialize=False)),
                ('quiz_0', models.JSONField(blank=True, db_column='quiz', null=True)),
                ('is_wrong', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'word_quiz',
                'managed': False,
            },
        ),
    ]
