# Generated by Django 3.2.8 on 2021-10-22 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0005_appointment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
