from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient
from apps.accounts.models import User, UserRole, EmployerProfile, CandidateProfile
from apps.jobs.models import Job, JobStatus
from apps.applications.models import Resume, JobApplication, ApplicationStatus
from apps.notifications.models import Notification

class ApplicationsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employer_user = User.objects.create_user(
            username="emp_app",
            email="emp_app@example.com",
            password="Password123!",
            role=UserRole.EMPLOYER
        )
        self.employer_profile = EmployerProfile.objects.get(user=self.employer_user)

        self.candidate_user = User.objects.create_user(
            username="cand_app",
            email="cand_app@example.com",
            password="Password123!",
            role=UserRole.CANDIDATE
        )
        self.candidate_profile = CandidateProfile.objects.get(user=self.candidate_user)

        self.job = Job.objects.create(
            employer=self.employer_profile,
            title="Fullstack Developer",
            description="Django + React",
            location="Remote",
            skills_required="Python, JavaScript",
            status=JobStatus.ACTIVE
        )

        self.resume_file = SimpleUploadedFile(
            "sample_resume.pdf",
            b"%PDF-1.4 sample pdf content",
            content_type="application/pdf"
        )
        self.resume = Resume.objects.create(
            candidate=self.candidate_profile,
            resume_file=self.resume_file
        )

        self.resume_upload_url = reverse('resume_upload')
        self.applications_url = reverse('application_list_create')

    def test_resume_pdf_validation(self):
        self.client.force_authenticate(user=self.candidate_user)

        # Non-PDF upload should fail validation
        bad_file = SimpleUploadedFile("doc.txt", b"text content", content_type="text/plain")
        res = self.client.post(self.resume_upload_url, {"resume_file": bad_file}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # PDF upload succeeds
        good_file = SimpleUploadedFile("my_resume.pdf", b"%PDF-1.4 test", content_type="application/pdf")
        res_ok = self.client.post(self.resume_upload_url, {"resume_file": good_file}, format='multipart')
        self.assertEqual(res_ok.status_code, status.HTTP_201_CREATED)

    def test_apply_for_job_and_prevent_duplicate_application(self):
        self.client.force_authenticate(user=self.candidate_user)
        payload = {
            "job_id": self.job.id,
            "resume_id": self.resume.id
        }

        # First application -> Success
        res1 = self.client.post(self.applications_url, payload)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertTrue(JobApplication.objects.filter(candidate=self.candidate_profile, job=self.job).exists())

        # Second application -> Fails with validation error
        res2 = self.client.post(self.applications_url, payload)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employer_update_application_status_and_notification(self):
        application = JobApplication.objects.create(
            candidate=self.candidate_profile,
            job=self.job,
            resume=self.resume,
            status=ApplicationStatus.APPLIED
        )

        self.client.force_authenticate(user=self.employer_user)
        status_url = reverse('application_status_update', kwargs={'pk': application.id})
        payload = {"status": "Shortlisted"}

        response = self.client.patch(status_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.SHORTLISTED)

        # Check that notification was generated for candidate user
        self.assertTrue(
            Notification.objects.filter(
                user=self.candidate_user,
                title__contains="Fullstack Developer"
            ).exists()
        )
