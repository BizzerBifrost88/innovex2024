# Generated by Django 5.1 on 2024-09-20 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KPMIM_Cafeteria_System', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('adminID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('phone', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('password', models.TextField()),
            ],
        ),
    ]
