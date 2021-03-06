# Generated by Django 2.0.3 on 2018-03-12 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nps', '0008_surveyaggregations_nps_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAggregations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_name', models.CharField(max_length=200)),
                ('product', models.CharField(max_length=30)),
                ('total_responses', models.IntegerField()),
                ('total_promoters', models.IntegerField()),
                ('percent_promoters', models.FloatField(blank=True, default=None, null=True)),
                ('total_detractors', models.IntegerField()),
                ('percent_detractors', models.FloatField(blank=True, default=None, null=True)),
                ('total_neutral', models.IntegerField()),
                ('percent_neutral', models.FloatField(blank=True, default=None, null=True)),
                ('number_clients_positive', models.IntegerField()),
                ('percent_clients_positive', models.FloatField(blank=True, default=None, null=True)),
                ('number_clients_negative', models.IntegerField()),
                ('percent_clients_negative', models.FloatField(blank=True, default=None, null=True)),
                ('number_clients_neutral', models.IntegerField()),
                ('percent_clients_neutral', models.FloatField(blank=True, default=None, null=True)),
                ('total_clients', models.IntegerField()),
                ('nps_score', models.FloatField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(max_length=30)),
                ('products', models.CharField(max_length=30)),
            ],
        ),
    ]
