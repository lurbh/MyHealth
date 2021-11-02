# Generated by Django 3.2.8 on 2021-10-12 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('systemadmin', '0002_auto_20211012_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='apptinterval',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='doctorinterval',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='openinghours',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='systemadmin.openinghours'),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
    ]