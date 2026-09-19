from django.urls import path
from .views import (
    ResumeListUploadView,
    ResumeDestroyView,
    CandidateApplicationListCreateView,
    JobApplicantsListView,
    ApplicationStatusUpdateView
)

urlpatterns = [
    path('resumes/upload/', ResumeListUploadView.as_view(), name='resume_upload'),
    path('resumes/', ResumeListUploadView.as_view(), name='resume_list'),
    path('resumes/<int:pk>/', ResumeDestroyView.as_view(), name='resume_destroy'),
    path('applications/', CandidateApplicationListCreateView.as_view(), name='application_list_create'),
    path('jobs/<int:job_id>/applicants/', JobApplicantsListView.as_view(), name='job_applicants'),
    path('applications/<int:pk>/status/', ApplicationStatusUpdateView.as_view(), name='application_status_update'),
]
