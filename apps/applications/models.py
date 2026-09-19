from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import CandidateProfile
from apps.jobs.models import Job
from apps.common.validators import validate_resume_file

class ApplicationStatus(models.TextChoices):
    APPLIED = 'Applied', _('Applied')
    UNDER_REVIEW = 'Under Review', _('Under Review')
    SHORTLISTED = 'Shortlisted', _('Shortlisted')
    INTERVIEW_SCHEDULED = 'Interview Scheduled', _('Interview Scheduled')
    SELECTED = 'Selected', _('Selected')
    REJECTED = 'Rejected', _('Rejected')

class Resume(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='resumes')
    resume_file = models.FileField(upload_to='resumes/%Y/%m/', validators=[validate_resume_file])
    file_type = models.CharField(max_length=50, default='application/pdf')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Resume of {self.candidate.user.username} uploaded {self.uploaded_at.strftime('%Y-%m-%d')}"

class JobApplication(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, related_name='applications')
    status = models.CharField(
        max_length=30,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.APPLIED
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('candidate', 'job')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.candidate.user.username} -> {self.job.title} ({self.status})"
