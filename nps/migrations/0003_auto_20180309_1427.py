# Generated by Django 2.0.3 on 2018-03-09 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nps', '0002_auto_20180308_1616'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='aggregatedresults',
            unique_together={('client', 'survey')},
        ),
        migrations.AlterUniqueTogether(
            name='rawresults',
            unique_together={('client', 'survey_name', 'question_name', 'user_id', 'response')},
        ),
    ]
