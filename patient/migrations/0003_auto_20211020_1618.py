# Generated by Django 3.2.8 on 2021-10-20 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinicadmin', '0006_appointmenttype_slot'),
        ('patient', '0002_rename_appointments_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinicadmin.room'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='slot',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='clinicadmin.slot'),
        ),
    ]
