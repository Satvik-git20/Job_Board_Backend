from django.urls import path
from .views import (
    JobListCreateView,
    JobDetailView,
    JobSearchView,
    EmployerJobsView,
    SavedJobListCreateView,
    SavedJobDestroyView
)

urlpatterns = [
    path('jobs/', JobListCreateView.as_view(), name='job_list_create'),
    path('jobs/search/', JobSearchView.as_view(), name='job_search'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('employer/jobs/', EmployerJobsView.as_view(), name='employer_jobs'),
    path('saved-jobs/', SavedJobListCreateView.as_view(), name='saved_job_list_create'),
    path('saved-jobs/<int:pk>/', SavedJobDestroyView.as_view(), name='saved_job_destroy'),
]
