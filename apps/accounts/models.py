from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class UserRole(models.TextChoices):
    CANDIDATE = 'candidate', _('Candidate')
    EMPLOYER = 'employer', _('Employer')
    ADMIN = 'admin', _('Admin')

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CANDIDATE
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return f"{self.username} ({self.role})"

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    full_name = models.CharField(max_length=255, blank=True, default='')
    phone = models.CharField(max_length=50, blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='')
    skills = models.TextField(blank=True, default='', help_text="Comma-separated list of skills e.g. Python, Django, REST API")
    experience_years = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True, default='')
    linkedin_url = models.URLField(max_length=500, blank=True, default='')
    github_url = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"Candidate Profile: {self.full_name or self.user.username}"

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255, blank=True, default='')
    company_description = models.TextField(blank=True, default='')
    website = models.URLField(max_length=500, blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='')
    industry = models.CharField(max_length=100, blank=True, default='')
    company_size = models.CharField(max_length=50, blank=True, default='', help_text="e.g. 1-10, 11-50, 50-200, 200+")

    def __str__(self):
        return f"Employer Profile: {self.company_name or self.user.username}"
