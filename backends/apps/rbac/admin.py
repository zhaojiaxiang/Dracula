from django.contrib import admin

from rbac.models import Group, Permission, Role, Organizations


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Organizations)
class OrganizationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'isgroup')
