# Generated by Django 2.0.3 on 2018-03-10 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nps', '0004_auto_20180309_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='question_name',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='question_type',
        ),
    ]