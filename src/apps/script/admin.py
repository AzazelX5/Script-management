from django.contrib import admin
from models import Script
# Register your models here.


class ScriptAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'creat_time')
    list_filter = ('creat_time',)


admin.site.register(Script, ScriptAdmin)