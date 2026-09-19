from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.accounts.models import User, UserRole
from apps.notifications.models import Notification

class NotificationsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="notif_user",
            email="notif@example.com",
            password="Password123!",
            role=UserRole.CANDIDATE
        )
        self.notification = Notification.objects.create(
            user=self.user,
            title="Application Shortlisted",
            message="Your application was shortlisted."
        )
        self.notif_list_url = reverse('notification_list')
        self.notif_read_url = reverse('notification_mark_read', kwargs={'pk': self.notification.id})

    def test_list_notifications(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get(self.notif_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)
        self.assertFalse(res.data['results'][0]['is_read'])

    def test_mark_notification_as_read(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.patch(self.notif_read_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
