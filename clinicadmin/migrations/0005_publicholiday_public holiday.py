# Generated by Django 3.2.8 on 2021-10-18 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicadmin', '0004_alter_doctorschedule_doctorid'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='publicholiday',
            constraint=models.UniqueConstraint(fields=('name', 'date'), name='Public Holiday'),
        ),
    ]