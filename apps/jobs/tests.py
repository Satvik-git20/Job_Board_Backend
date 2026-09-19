from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.accounts.models import User, UserRole, EmployerProfile, CandidateProfile
from apps.jobs.models import Job, JobStatus, JobType, SavedJob

class JobsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employer_user = User.objects.create_user(
            username="emp_test",
            email="emp@example.com",
            password="Password123!",
            role=UserRole.EMPLOYER
        )
        self.employer_profile = EmployerProfile.objects.get(user=self.employer_user)
        self.employer_profile.company_name = "TechCorp"
        self.employer_profile.save()

        self.candidate_user = User.objects.create_user(
            username="cand_test",
            email="cand@example.com",
            password="Password123!",
            role=UserRole.CANDIDATE
        )
        self.candidate_profile = CandidateProfile.objects.get(user=self.candidate_user)

        self.job_list_url = reverse('job_list_create')
        self.job_search_url = reverse('job_search')
        self.saved_jobs_url = reverse('saved_job_list_create')

    def test_employer_create_job(self):
        self.client.force_authenticate(user=self.employer_user)
        payload = {
            "title": "Senior Python Developer",
            "description": "Building scalable backend services with Django.",
            "location": "Remote",
            "salary_min": 100000.00,
            "salary_max": 140000.00,
            "experience_required": 5,
            "job_type": "full_time",
            "skills_required": "Python, Django, PostgreSQL",
            "openings": 2,
            "status": "active"
        }
        response = self.client.post(self.job_list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 1)

    def test_candidate_cannot_create_job(self):
        self.client.force_authenticate(user=self.candidate_user)
        payload = {
            "title": "Fake Job",
            "description": "Invalid",
            "location": "Remote",
            "skills_required": "Python"
        }
        response = self.client.post(self.job_list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_job_search_and_filtering(self):
        Job.objects.create(
            employer=self.employer_profile,
            title="Django Backend Engineer",
            description="Django REST Framework developer",
            location="San Francisco",
            salary_min=120000,
            salary_max=150000,
            experience_required=3,
            job_type=JobType.FULL_TIME,
            skills_required="Django, Python, Celery",
            status=JobStatus.ACTIVE
        )
        Job.objects.create(
            employer=self.employer_profile,
            title="React Frontend Developer",
            description="Frontend React JS developer",
            location="New York",
            salary_min=90000,
            salary_max=110000,
            experience_required=2,
            job_type=JobType.REMOTE,
            skills_required="React, JavaScript",
            status=JobStatus.ACTIVE
        )

        # Filter by location
        res = self.client.get(f"{self.job_list_url}?location=San Francisco")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)
        self.assertEqual(res.data['results'][0]['title'], "Django Backend Engineer")

        # Filter by min_salary
        res_sal = self.client.get(f"{self.job_list_url}?min_salary=100000")
        self.assertEqual(res_sal.data['count'], 1)

        # Search endpoint
        res_search = self.client.get(f"{self.job_search_url}?search=React")
        self.assertEqual(res_search.data['count'], 1)
        self.assertEqual(res_search.data['results'][0]['title'], "React Frontend Developer")

    def test_candidate_save_and_unsave_job(self):
        job = Job.objects.create(
            employer=self.employer_profile,
            title="DevOps Engineer",
            description="AWS Kubernetes",
            location="Remote",
            skills_required="AWS, Docker",
            status=JobStatus.ACTIVE
        )
        self.client.force_authenticate(user=self.candidate_user)

        # Save job
        save_res = self.client.post(self.saved_jobs_url, {"job_id": job.id})
        self.assertEqual(save_res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(SavedJob.objects.filter(candidate=self.candidate_profile, job=job).exists())

        saved_job_id = save_res.data['id']
        destroy_url = reverse('saved_job_destroy', kwargs={'pk': saved_job_id})
        del_res = self.client.delete(destroy_url)
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SavedJob.objects.filter(candidate=self.candidate_profile, job=job).exists())
