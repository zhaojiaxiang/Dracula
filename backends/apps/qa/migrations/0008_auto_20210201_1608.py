# Generated by Django 2.2.14 on 2021-02-01 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0007_auto_20210120_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='qahead',
            name='fslipno2',
            field=models.IntegerField(default=1, verbose_name='订单支号（应用于PCL）'),
        ),
        migrations.AlterField(
            model_name='qahead',
            name='fslipno',
            field=models.CharField(max_length=20, verbose_name='联络票号/订单号'),
        ),
    ]
