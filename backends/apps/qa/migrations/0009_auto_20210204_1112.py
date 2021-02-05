# Generated by Django 2.2.14 on 2021-02-04 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0008_auto_20210201_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qadetail',
            name='fclass1',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True, verbose_name='分类1'),
        ),
        migrations.AlterField(
            model_name='qadetail',
            name='fregression',
            field=models.CharField(db_index=True, default='N', max_length=1, verbose_name='回归测试'),
        ),
        migrations.AlterField(
            model_name='qadetail',
            name='fresult',
            field=models.CharField(blank=True, db_index=True, max_length=10, null=True, verbose_name='测试结果'),
        ),
        migrations.AlterField(
            model_name='qadetail',
            name='fsortrule',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='排序规则'),
        ),
        migrations.AlterField(
            model_name='qahead',
            name='fobjectid',
            field=models.CharField(db_index=True, max_length=50, verbose_name='测试对象'),
        ),
        migrations.AlterField(
            model_name='qahead',
            name='fslipno',
            field=models.CharField(db_index=True, max_length=20, verbose_name='联络票号/订单号'),
        ),
        migrations.AlterField(
            model_name='qahead',
            name='fslipno2',
            field=models.IntegerField(db_index=True, default=1, verbose_name='订单支号（应用于PCL）'),
        ),
        migrations.AlterField(
            model_name='qahead',
            name='ftesttyp',
            field=models.CharField(db_index=True, max_length=6, verbose_name='测试类型'),
        ),
    ]
