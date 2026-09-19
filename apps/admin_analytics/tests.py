from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.accounts.models import User, UserRole

class AdminAnalyticsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin_user",
            email="admin@example.com",
            password="Password123!",
            role=UserRole.ADMIN,
            is_staff=True
        )
        self.candidate_user = User.objects.create_user(
            username="cand_user",
            email="cand_user@example.com",
            password="Password123!",
            role=UserRole.CANDIDATE
        )
        self.stats_url = reverse('admin_stats')

    def test_admin_can_access_stats(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("users", response.data)
        self.assertIn("jobs", response.data)
        self.assertIn("applications", response.data)

    def test_candidate_forbidden_from_admin_stats(self):
        self.client.force_authenticate(user=self.candidate_user)
        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
