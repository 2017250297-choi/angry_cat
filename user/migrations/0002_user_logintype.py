# Generated by Django 4.2.1 on 2023-05-26 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='logintype',
            field=models.CharField(choices=[('GOOGLE', 'GOOGLE'), ('LOCAL', 'LOCAL')], default='LOCAL', max_length=6),
        ),
    ]
