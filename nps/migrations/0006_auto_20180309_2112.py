# Generated by Django 2.0.3 on 2018-03-10 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nps', '0005_auto_20180309_2017'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyAggregations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_name', models.CharField(max_length=200)),
                ('total_responses', models.IntegerField()),
                ('total_promoters', models.IntegerField()),
                ('percent_promoters', models.FloatField(blank=True, default=None, null=True)),
                ('total_detractors', models.IntegerField()),
                ('total_neutral', models.IntegerField()),
                ('percent_neutral', models.FloatField(blank=True, default=None, null=True)),
                ('number_clients_positive', models.IntegerField()),
                ('percent_clients_positive', models.FloatField(blank=True, default=None, null=True)),
                ('number_clients_negative', models.IntegerField()),
                ('percent_clients_negative', models.FloatField(blank=True, default=None, null=True)),
                ('number_clients_neutral', models.IntegerField()),
                ('percent_clients_neutral', models.FloatField(blank=True, default=None, null=True)),
                ('total_clients', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='aggregatedresults',
            name='percent_detractors',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='aggregatedresults',
            name='percent_neutral',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='aggregatedresults',
            name='percent_promoters',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='commentanalysis',
            name='sentiment',
            field=models.CharField(choices=[('-1', 'Negative'), ('0', 'Neutral'), ('1', 'Positive'), ('', 'Unknown')], max_length=10),
        ),
    ]
