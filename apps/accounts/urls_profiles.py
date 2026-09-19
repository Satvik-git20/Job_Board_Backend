from django.urls import path
from .views import CandidateProfileView, EmployerProfileView

urlpatterns = [
    path('candidate/profile/', CandidateProfileView.as_view(), name='candidate_profile'),
    path('employer/profile/', EmployerProfileView.as_view(), name='employer_profile'),
]
