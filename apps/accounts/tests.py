from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.accounts.models import User, UserRole, CandidateProfile, EmployerProfile

class AccountsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('auth_register')
        self.login_url = reverse('auth_login')
        self.logout_url = reverse('auth_logout')
        self.change_password_url = reverse('auth_change_password')
        self.candidate_profile_url = reverse('candidate_profile')
        self.employer_profile_url = reverse('employer_profile')

    def test_register_candidate(self):
        payload = {
            "username": "candidate1",
            "email": "candidate1@example.com",
            "password": "Password123!",
            "password_confirm": "Password123!",
            "role": "candidate"
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("tokens", response.data)
        self.assertTrue(User.objects.filter(email="candidate1@example.com").exists())
        self.assertTrue(CandidateProfile.objects.filter(user__username="candidate1").exists())

    def test_register_employer(self):
        payload = {
            "username": "employer1",
            "email": "employer1@example.com",
            "password": "Password123!",
            "password_confirm": "Password123!",
            "role": "employer"
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(EmployerProfile.objects.filter(user__username="employer1").exists())

    def test_login_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Password123!",
            role=UserRole.CANDIDATE
        )
        payload = {
            "username_or_email": "test@example.com",
            "password": "Password123!"
        }
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tokens", response.data)
        access_token = response.data["tokens"]["access"]

        # Test authenticated candidate profile retrieve
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        prof_res = self.client.get(self.candidate_profile_url)
        self.assertEqual(prof_res.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        user = User.objects.create_user(
            username="pwduser",
            email="pwduser@example.com",
            password="OldPassword123!",
            role=UserRole.CANDIDATE
        )
        login_res = self.client.post(self.login_url, {
            "username_or_email": "pwduser",
            "password": "OldPassword123!"
        })
        access_token = login_res.data["tokens"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        change_payload = {
            "old_password": "OldPassword123!",
            "new_password": "NewPassword123!",
            "new_password_confirm": "NewPassword123!"
        }
        res = self.client.post(self.change_password_url, change_payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Verify new password works
        self.client.credentials()
        login_res2 = self.client.post(self.login_url, {
            "username_or_email": "pwduser",
            "password": "NewPassword123!"
        })
        self.assertEqual(login_res2.status_code, status.HTTP_200_OK)
