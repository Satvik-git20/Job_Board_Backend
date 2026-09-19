from django.urls import path
from .views import AdminPlatformStatsView

urlpatterns = [
    path('stats/', AdminPlatformStatsView.as_view(), name='admin_stats'),
]
