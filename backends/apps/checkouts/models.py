from django.db import models

from accounts.models import User


class CheckOutFiles(models.Model):
    """
    程序管理记录
    """
    fregisterdte = models.DateField(verbose_name='申请日期', auto_now_add=True)
    fsystem = models.CharField(verbose_name='系统名称', max_length=6)
    fcomment = models.CharField(verbose_name='备注', max_length=100)
    fslipno = models.CharField(verbose_name='联络票号', max_length=20)
    fchkoutobj = models.CharField(verbose_name='迁出对象', max_length=40)
    fapplicant = models.CharField(verbose_name='申请者', max_length=20)
    fchkstatus = models.CharField(verbose_name='状态', max_length=20)
    fchkoutperson = models.CharField(verbose_name='迁出者', max_length=20, null=True, blank=True)
    fchkoutdte = models.DateField(verbose_name='迁出日期', null=True, blank=True)
    fchkoutfile = models.CharField(verbose_name='PBL名称', max_length=40, null=True, blank=True)
    fchkinperson = models.CharField(verbose_name='迁入者', max_length=20, null=True, blank=True)
    fchkindte = models.DateField(verbose_name='迁入日期', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'checkouts'
        verbose_name = '程序迁出记录'
        verbose_name_plural = verbose_name


class Recipients(models.Model):
    """
    迁出程序邮件接收者
    """
    email = models.EmailField(verbose_name='邮箱', max_length=64)
    name = models.CharField(verbose_name='收件者', max_length=64)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'recipients'
        verbose_name = '程序管理记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email
