from django.contrib import admin
from .models import Job, SavedJob

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'location', 'job_type', 'status', 'created_at')
    list_filter = ('job_type', 'status', 'created_at', 'location')
    search_fields = ('title', 'description', 'employer__company_name', 'skills_required')
    ordering = ('-created_at',)

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'saved_at')
    search_fields = ('candidate__user__username', 'job__title')
