from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import EmployerProfile, CandidateProfile

class JobType(models.TextChoices):
    FULL_TIME = 'full_time', _('Full-time')
    PART_TIME = 'part_time', _('Part-time')
    CONTRACT = 'contract', _('Contract')
    INTERNSHIP = 'internship', _('Internship')
    REMOTE = 'remote', _('Remote')

class JobStatus(models.TextChoices):
    ACTIVE = 'active', _('Active')
    CLOSED = 'closed', _('Closed')

class Job(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    experience_required = models.PositiveIntegerField(default=0, help_text="Years of experience required")
    job_type = models.CharField(max_length=20, choices=JobType.choices, default=JobType.FULL_TIME)
    skills_required = models.TextField(help_text="Comma-separated skills e.g. Python, Django, PostgreSQL")
    openings = models.PositiveIntegerField(default=1)
    application_deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=JobStatus.choices, default=JobStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.employer.company_name or self.employer.user.username}"

class SavedJob(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by_candidates')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidate', 'job')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.candidate.user.username} saved {self.job.title}"
