from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Resume, JobApplication
from .serializers import (
    ResumeSerializer,
    JobApplicationSerializer,
    JobApplicationCreateSerializer,
    JobApplicationStatusUpdateSerializer
)
from apps.jobs.models import Job
from apps.common.permissions import IsCandidate, IsEmployer, IsCandidateOwner, IsEmployerOwner
from apps.notifications.tasks import send_application_status_notification

class ResumeListUploadView(generics.ListCreateAPIView):
    """
    POST /api/resumes/upload
    GET /api/resumes
    Upload candidate resume (PDF only, <= 5MB).
    """
    permission_classes = [permissions.IsAuthenticated, IsCandidate]
    serializer_class = ResumeSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return Resume.objects.filter(candidate=self.request.user.candidate_profile)

class ResumeDestroyView(generics.DestroyAPIView):
    """
    DELETE /api/resumes/{id}
    """
    permission_classes = [permissions.IsAuthenticated, IsCandidate, IsCandidateOwner]
    serializer_class = ResumeSerializer

    def get_queryset(self):
        return Resume.objects.filter(candidate=self.request.user.candidate_profile)

class CandidateApplicationListCreateView(generics.ListCreateAPIView):
    """
    GET /api/applications - List all applications submitted by candidate
    POST /api/applications - Apply for a job
    """
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobApplicationCreateSerializer
        return JobApplicationSerializer

    def get_queryset(self):
        return JobApplication.objects.filter(
            candidate=self.request.user.candidate_profile
        ).select_related('candidate', 'candidate__user', 'job', 'job__employer', 'resume')

class JobApplicantsListView(generics.ListAPIView):
    """
    GET /api/jobs/{id}/applicants
    List all candidate applicants for a specific job posted by the employer.
    """
    permission_classes = [permissions.IsAuthenticated, IsEmployer]
    serializer_class = JobApplicationSerializer

    def get_queryset(self):
        job_id = self.kwargs.get('job_id')
        return JobApplication.objects.filter(
            job_id=job_id,
            job__employer=self.request.user.employer_profile
        ).select_related('candidate', 'candidate__user', 'job', 'resume')

class ApplicationStatusUpdateView(generics.UpdateAPIView):
    """
    PATCH /api/applications/{id}/status
    Employer updates the status of an application for one of their jobs.
    Triggers asynchronous notification to the candidate.
    """
    permission_classes = [permissions.IsAuthenticated, IsEmployer]
    serializer_class = JobApplicationStatusUpdateSerializer
    http_method_names = ['patch']

    def get_queryset(self):
        return JobApplication.objects.filter(
            job__employer=self.request.user.employer_profile
        )

    def perform_update(self, serializer):
        application = serializer.save()
        new_status = application.status
        job_title = application.job.title
        candidate_user_id = application.candidate.user.id

        # Trigger Celery notification task asynchronously
        send_application_status_notification.delay(
            user_id=candidate_user_id,
            job_title=job_title,
            new_status=new_status
        )
