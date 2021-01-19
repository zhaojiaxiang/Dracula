from django.db import models

from DjangoUeditor.models import UEditorField


class CodeReview(models.Model):
    fslipno = models.CharField(verbose_name='联络票号', max_length=20)
    fobjectid = models.CharField(verbose_name='Review对象', max_length=100)
    fcontent_text = UEditorField(verbose_name='Review内容', imagePath="code_review/images/%Y%m/", width=1000, height=300,
                                 filePath="code_review/files/%Y%m/", default='')
    fentdt = models.DateField(verbose_name='登入日期', auto_now_add=True)
    fentusr = models.CharField(verbose_name='登录者', max_length=24, null=True, blank=True)
    fupdtedt = models.DateField(verbose_name='更新日期', null=True, blank=True)
    fupdteusr = models.CharField(verbose_name='更新者', max_length=24, null=True, blank=True)
    fupdteprg = models.CharField(verbose_name='更新程序名', max_length=110, null=True, blank=True)

    class Meta:
        db_table = 'codereview'
        verbose_name = '代码Review'
        verbose_name_plural = verbose_name


class DesignReview(models.Model):
    fslipno = models.CharField(verbose_name='联络票号', max_length=20)
    fcontent_text = UEditorField(verbose_name='Review内容', imagePath="design_review/images/%Y%m/", width=1000, height=300,
                                 filePath="design_review/files/%Y%m/", default='')
    fentdt = models.DateField(verbose_name='登入日期', auto_now_add=True)
    fentusr = models.CharField(verbose_name='登录者', max_length=24, null=True, blank=True)
    fupdtedt = models.DateField(verbose_name='更新日期', null=True, blank=True)
    fupdteusr = models.CharField(verbose_name='更新者', max_length=24, null=True, blank=True)
    fupdteprg = models.CharField(verbose_name='更新程序名', max_length=110, null=True, blank=True)

    class Meta:
        db_table = 'designreview'
        verbose_name = '设计Review'
        verbose_name_plural = verbose_name
