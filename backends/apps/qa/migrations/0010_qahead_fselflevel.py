# Generated by Django 2.2.14 on 2021-03-02 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0009_auto_20210204_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='qahead',
            name='fselflevel',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='自我评价难易等级'),
        ),
    ]