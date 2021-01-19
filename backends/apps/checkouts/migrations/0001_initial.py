# Generated by Django 2.2.14 on 2020-11-10 06:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=64, verbose_name='邮箱')),
                ('name', models.CharField(max_length=64, verbose_name='收件者')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '程序管理记录',
                'verbose_name_plural': '程序管理记录',
                'db_table': 'recipients',
            },
        ),
        migrations.CreateModel(
            name='CheckOutFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fregisterdte', models.DateField(auto_now_add=True, verbose_name='申请日期')),
                ('fsystem', models.CharField(max_length=6, verbose_name='系统名称')),
                ('fcomment', models.CharField(max_length=100, verbose_name='备注')),
                ('fslipno', models.CharField(max_length=20, verbose_name='联络票号')),
                ('fchkoutobj', models.CharField(max_length=40, verbose_name='迁出对象')),
                ('fapplicant', models.CharField(max_length=20, verbose_name='申请者')),
                ('fchkstatus', models.CharField(max_length=20, verbose_name='状态')),
                ('fchkoutperson', models.CharField(blank=True, max_length=20, null=True, verbose_name='迁出者')),
                ('fchkoutdte', models.DateField(blank=True, null=True, verbose_name='迁出日期')),
                ('fchkoutfile', models.CharField(blank=True, max_length=40, null=True, verbose_name='PBL名称')),
                ('fchkinperson', models.CharField(blank=True, max_length=20, null=True, verbose_name='迁入者')),
                ('fchkindte', models.DateField(blank=True, null=True, verbose_name='迁入日期')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '程序迁出记录',
                'verbose_name_plural': '程序迁出记录',
                'db_table': 'checkouts',
            },
        ),
    ]
