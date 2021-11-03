# Generated by Django 3.2.8 on 2021-10-23 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicadmin', '0007_slot_occupied'),
    ]

    operations = [
        migrations.RenameField(
            model_name='slot',
            old_name='datetime',
            new_name='datetimestart',
        ),
        migrations.AddField(
            model_name='slot',
            name='datetimeend',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 24, 0, 10, 6, 85626)),
        ),
    ]
