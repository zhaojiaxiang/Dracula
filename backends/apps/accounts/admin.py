from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, SystemSetting


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'name', 'username', 'email', 'ammic_group', 'ammic_organization', 'is_superuser', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal Info'), {'fields': ('name', 'email', 'avatar', 'ammic_group', 'ammic_role', 'ammic_organization')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = ((None, {
        'classes': ('wide',),
        'fields': ('username', 'name', 'password1', 'password2', 'email', 'is_active',
                   'is_staff', 'ammic_group', 'ammic_role', 'ammic_organization'),
    }),
                     )


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('type', 'picture', 'title', 'description', 'router')
