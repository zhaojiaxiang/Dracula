# Generated by Django 2.2.14 on 2020-12-30 08:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_systemsetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemsetting',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='systemsetting',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
    ]
