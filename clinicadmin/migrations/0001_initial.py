# Generated by Django 3.2.8 on 2021-10-14 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('systemadmin', '0007_auto_20211014_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotionalMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('senddate', models.DateTimeField(auto_now_add=True)),
                ('clinicid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systemadmin.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='EducationMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.FileField(upload_to='files/educationmaterials')),
                ('uploaddate', models.DateTimeField(auto_now_add=True)),
                ('clinicid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systemadmin.clinic')),
            ],
        ),
    ]
