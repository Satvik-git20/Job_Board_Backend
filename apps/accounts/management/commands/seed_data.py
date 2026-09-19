from django.core.management.base import BaseCommand
from apps.accounts.models import User, UserRole, CandidateProfile, EmployerProfile
from apps.jobs.models import Job, JobStatus, JobType
from apps.applications.models import Resume, JobApplication, ApplicationStatus
from apps.notifications.models import Notification
from django.core.files.uploadedfile import SimpleUploadedFile

class Command(BaseCommand):
    help = 'Seeds initial sample data for Job Board platform'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding sample data...")

        # 1. Admin User
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@jobboard.com',
                'role': UserRole.ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'is_verified': True
            }
        )
        if created:
            admin_user.set_password('Admin@123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created Admin: admin / Admin@123"))

        # 2. Employer User
        emp_user, created = User.objects.get_or_create(
            username='techcorp_emp',
            defaults={
                'email': 'hr@techcorp.com',
                'role': UserRole.EMPLOYER,
                'is_verified': True
            }
        )
        if created:
            emp_user.set_password('Employer@123')
            emp_user.save()
            self.stdout.write(self.style.SUCCESS("Created Employer: techcorp_emp / Employer@123"))

        emp_profile, _ = EmployerProfile.objects.get_or_create(user=emp_user)
        emp_profile.company_name = "TechCorp Solutions"
        emp_profile.company_description = "Leading enterprise software and cloud engineering firm."
        emp_profile.website = "https://techcorp.example.com"
        emp_profile.location = "San Francisco, CA"
        emp_profile.industry = "Software Development"
        emp_profile.company_size = "50-200"
        emp_profile.save()

        # 3. Candidate User
        cand_user, created = User.objects.get_or_create(
            username='john_cand',
            defaults={
                'email': 'john.doe@example.com',
                'role': UserRole.CANDIDATE,
                'is_verified': True
            }
        )
        if created:
            cand_user.set_password('Candidate@123')
            cand_user.save()
            self.stdout.write(self.style.SUCCESS("Created Candidate: john_cand / Candidate@123"))

        cand_profile, _ = CandidateProfile.objects.get_or_create(user=cand_user)
        cand_profile.full_name = "John Doe"
        cand_profile.phone = "+1-555-0192"
        cand_profile.location = "Austin, TX"
        cand_profile.skills = "Python, Django, PostgreSQL, Docker, Redis, REST API"
        cand_profile.experience_years = 4
        cand_profile.bio = "Experienced Full-stack and Backend Python engineer passionate about scalable systems."
        cand_profile.linkedin_url = "https://linkedin.com/in/johndoe"
        cand_profile.github_url = "https://github.com/johndoe"
        cand_profile.save()

        # 4. Jobs
        job1, _ = Job.objects.get_or_create(
            employer=emp_profile,
            title="Senior Backend Engineer (Python/Django)",
            defaults={
                'description': "We are seeking a Senior Backend Engineer to architect microservices and high-throughput APIs.",
                'location': "Remote",
                'salary_min': 120000.00,
                'salary_max': 160000.00,
                'experience_required': 4,
                'job_type': JobType.REMOTE,
                'skills_required': "Python, Django, PostgreSQL, Celery, Redis",
                'openings': 3,
                'status': JobStatus.ACTIVE
            }
        )

        job2, _ = Job.objects.get_or_create(
            employer=emp_profile,
            title="DevOps & Cloud Engineer",
            defaults={
                'description': "Manage AWS infrastructure, CI/CD pipelines, and Kubernetes deployments.",
                'location': "San Francisco, CA",
                'salary_min': 130000.00,
                'salary_max': 170000.00,
                'experience_required': 3,
                'job_type': JobType.FULL_TIME,
                'skills_required': "AWS, Kubernetes, Terraform, Docker",
                'openings': 1,
                'status': JobStatus.ACTIVE
            }
        )

        # 5. Resume
        sample_pdf = SimpleUploadedFile("john_doe_resume.pdf", b"%PDF-1.4 Sample Resume Content", content_type="application/pdf")
        resume, _ = Resume.objects.get_or_create(
            candidate=cand_profile,
            defaults={'resume_file': sample_pdf, 'file_type': 'application/pdf'}
        )

        # 6. Job Application
        app, _ = JobApplication.objects.get_or_create(
            candidate=cand_profile,
            job=job1,
            defaults={'resume': resume, 'status': ApplicationStatus.SHORTLISTED}
        )

        # 7. Notification
        Notification.objects.get_or_create(
            user=cand_user,
            title="Application Shortlisted!",
            defaults={'message': f"Your application for '{job1.title}' at TechCorp Solutions has been shortlisted!"}
        )

        self.stdout.write(self.style.SUCCESS("Sample seed data created successfully!"))
