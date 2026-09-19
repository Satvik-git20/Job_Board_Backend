from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.db.models import Count
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.accounts.models import User, UserRole
from apps.jobs.models import Job, JobStatus
from apps.applications.models import JobApplication, ApplicationStatus
from apps.common.permissions import IsAdminUserRole

class AdminPlatformStatsView(APIView):
    """
    GET /api/admin/stats
    Returns overall platform statistics and report metrics for Admin users.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminUserRole]

    @extend_schema(
        responses={200: OpenApiResponse(description="Returns aggregated platform statistics.")}
    )
    def get(self, request):
        total_users = User.objects.count()
        candidates_count = User.objects.filter(role=UserRole.CANDIDATE).count()
        employers_count = User.objects.filter(role=UserRole.EMPLOYER).count()
        admins_count = User.objects.filter(role=UserRole.ADMIN).count()

        total_jobs = Job.objects.count()
        active_jobs = Job.objects.filter(status=JobStatus.ACTIVE).count()
        closed_jobs = Job.objects.filter(status=JobStatus.CLOSED).count()

        total_applications = JobApplication.objects.count()
        applications_by_status = dict(
            JobApplication.objects.values('status').annotate(count=Count('id')).values_list('status', 'count')
        )

        return Response({
            "users": {
                "total": total_users,
                "candidates": candidates_count,
                "employers": employers_count,
                "admins": admins_count,
            },
            "jobs": {
                "total": total_jobs,
                "active": active_jobs,
                "closed": closed_jobs,
            },
            "applications": {
                "total": total_applications,
                "breakdown": applications_by_status
            }
        }, status=status.HTTP_200_OK)
