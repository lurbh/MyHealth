# Generated by Django 3.2.8 on 2021-11-03 14:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicadmin', '0010_alter_slot_datetimeend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='datetimeend',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 3, 22, 48, 45, 883285)),
        ),
    ]