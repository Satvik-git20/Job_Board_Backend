from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Job, SavedJob, JobStatus
from .filters import JobFilter
from .serializers import JobSerializer, JobCreateUpdateSerializer, SavedJobSerializer
from apps.common.permissions import IsEmployer, IsCandidate, IsEmployerOwner, IsCandidateOwner

@extend_schema_view(
    get=extend_schema(description="List active jobs with filters, search, and pagination."),
    post=extend_schema(description="Create a new job posting (Employer only).")
)
class JobListCreateView(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'skills_required', 'employer__company_name', 'location']
    ordering_fields = ['created_at', 'salary_min', 'salary_max', 'experience_required']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsEmployer()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        if self.request.method == 'POST':
            return Job.objects.all()
        # Public listing defaults to active jobs unless admin or specified
        return Job.objects.filter(status=JobStatus.ACTIVE).select_related('employer', 'employer__user')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobCreateUpdateSerializer
        return JobSerializer

    def perform_create(self, serializer):
        employer_profile = self.request.user.employer_profile
        serializer.save(employer=employer_profile)


@extend_schema_view(
    get=extend_schema(description="Get details of a specific job."),
    put=extend_schema(description="Update job details (Employer owner only)."),
    patch=extend_schema(description="Partial update job details (Employer owner only)."),
    delete=extend_schema(description="Delete a job (Employer owner only).")
)
class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.select_related('employer', 'employer__user').all()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsEmployer(), IsEmployerOwner()]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return JobSerializer
        return JobCreateUpdateSerializer


class JobSearchView(generics.ListAPIView):
    """
    Dedicated Search Endpoint for Jobs
    GET /api/jobs/search
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'skills_required', 'employer__company_name', 'location']
    ordering_fields = ['created_at', 'salary_min', 'salary_max', 'experience_required']
    ordering = ['-created_at']

    def get_queryset(self):
        return Job.objects.filter(status=JobStatus.ACTIVE).select_related('employer', 'employer__user')


class EmployerJobsView(generics.ListAPIView):
    """
    GET /api/employer/jobs
    Retrieves all jobs created by the authenticated employer.
    """
    permission_classes = [permissions.IsAuthenticated, IsEmployer]
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'skills_required']
    ordering = ['-created_at']

    def get_queryset(self):
        return Job.objects.filter(employer=self.request.user.employer_profile).select_related('employer')


class SavedJobListCreateView(generics.ListCreateAPIView):
    """
    GET /api/saved-jobs
    POST /api/saved-jobs
    Candidate only API for saving & viewing saved jobs.
    """
    permission_classes = [permissions.IsAuthenticated, IsCandidate]
    serializer_class = SavedJobSerializer

    def get_queryset(self):
        return SavedJob.objects.filter(candidate=self.request.user.candidate_profile).select_related('job', 'job__employer')


class SavedJobDestroyView(generics.DestroyAPIView):
    """
    DELETE /api/saved-jobs/{id}
    Removes a saved job by ID.
    """
    permission_classes = [permissions.IsAuthenticated, IsCandidate, IsCandidateOwner]
    serializer_class = SavedJobSerializer

    def get_queryset(self):
        return SavedJob.objects.filter(candidate=self.request.user.candidate_profile)
