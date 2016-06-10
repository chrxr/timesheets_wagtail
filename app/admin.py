from django.contrib import admin
from .models import Project, WorkDay
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    pass

class WorkDayAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)
admin.site.register(WorkDay, WorkDayAdmin)
