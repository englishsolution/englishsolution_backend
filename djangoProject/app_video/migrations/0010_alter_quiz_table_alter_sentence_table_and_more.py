# Generated by Django 5.0.6 on 2024-07-13 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_video', '0009_alter_sentence_options'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='quiz',
            table='quiz',
        ),
        migrations.AlterModelTable(
            name='sentence',
            table='sentence',
        ),
        migrations.AlterModelTable(
            name='sentencequiz',
            table='sentence_quiz',
        ),
        migrations.AlterModelTable(
            name='test',
            table='test',
        ),
        migrations.AlterModelTable(
            name='users',
            table='users',
        ),
        migrations.AlterModelTable(
            name='video',
            table='video',
        ),
        migrations.AlterModelTable(
            name='word',
            table='word',
        ),
        migrations.AlterModelTable(
            name='wordquiz',
            table='word_quiz',
        ),
    ]
