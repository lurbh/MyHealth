# Generated by Django 3.2.8 on 2021-10-12 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systemadmin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='type',
            field=models.CharField(choices=[('normal', 'Normal'), ('specialist', 'Specialist')], default='normal', max_length=100),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='location',
            field=models.CharField(choices=[('north', 'North'), ('south', 'South'), ('central', 'Central'), ('east', 'East'), ('west', 'West')], default='central', max_length=100),
        ),
    ]
