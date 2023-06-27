from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


class TeacherAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser']


admin.site.register(models.Teacher, TeacherAdmin)
admin.site.register(models.Student)
admin.site.register(models.Klass)
admin.site.register(models.School)
