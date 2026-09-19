from django.contrib import admin
from .models import Resume, JobApplication

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'file_type', 'uploaded_at')
    search_fields = ('candidate__user__username', 'candidate__full_name')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'status', 'applied_at', 'updated_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('candidate__user__username', 'job__title', 'job__employer__company_name')
