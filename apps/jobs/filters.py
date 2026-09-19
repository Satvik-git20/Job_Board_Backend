import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    min_salary = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gte')
    max_salary = django_filters.NumberFilter(field_name='salary_max', lookup_expr='lte')
    experience = django_filters.NumberFilter(field_name='experience_required', lookup_expr='lte')
    job_type = django_filters.CharFilter(field_name='job_type', lookup_expr='exact')
    skills = django_filters.CharFilter(field_name='skills_required', lookup_expr='icontains')
    company = django_filters.CharFilter(field_name='employer__company_name', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')

    class Meta:
        model = Job
        fields = ['location', 'min_salary', 'max_salary', 'experience', 'job_type', 'skills', 'company', 'status']
