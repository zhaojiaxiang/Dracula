from django.db import models


class Permission(models.Model):
    """
    URL权限表
    """
    name = models.CharField(verbose_name='标题', max_length=128)
    url = models.CharField(verbose_name='含正则的URL', max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "permissions"
        verbose_name = "权限"
        verbose_name_plural = verbose_name


class Role(models.Model):
    """
    角色
    """
    name = models.CharField(verbose_name='角色名称', max_length=32)
    permission = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "roles"
        verbose_name = "角色"
        verbose_name_plural = verbose_name


class Group(models.Model):
    """
    组别
    """
    name = models.CharField(verbose_name='组名', max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "groups"
        verbose_name = "组别"
        verbose_name_plural = verbose_name

