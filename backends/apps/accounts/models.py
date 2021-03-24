from django.contrib.auth.models import AbstractUser
from django.db import models

from rbac.models import Role, Group, Organizations


class User(AbstractUser):
    """ 用户的基本信息表 """
    name = models.CharField(max_length=30, null=True,
                            unique=True, verbose_name="姓名",
                            error_messages={
                                'unique': '姓名已经在系统中存在'
                            })
    email = models.EmailField(max_length=100, verbose_name="邮箱",
                              unique=True,
                              error_messages={
                                  'unique': '邮箱已经在系统中存在'
                              })
    avatar = models.ImageField(verbose_name='用户头像', upload_to='avatar/', null=True, blank=True)
    ammic_group = models.ForeignKey(Group, verbose_name="开发组", related_name='ammic_group', null=True,
                                    blank=True, on_delete=models.DO_NOTHING)

    ammic_role = models.ManyToManyField(Role, verbose_name='拥有的所有角色',
                                        related_name='ammic_role')

    ammic_organization = models.ForeignKey(Organizations, verbose_name="组织架构", related_name='ammic_organization',
                                           on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class SystemSetting(models.Model):
    type = models.CharField(verbose_name="配置类型", max_length=30)
    picture = models.ImageField(verbose_name="配置图片", upload_to='settings/', null=True, blank=True)
    title = models.CharField(verbose_name="配置标题", max_length=64)
    description = models.CharField(verbose_name="配置描述", max_length=64, null=True, blank=True)
    router = models.URLField(verbose_name="配置路由", null=True, blank=True)
    user = models.ForeignKey(User, "配置者", related_name="setting_user")
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        db_table = 'settings'
        verbose_name = '系统配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
