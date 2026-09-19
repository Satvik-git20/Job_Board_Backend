from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserRole, CandidateProfile, EmployerProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == UserRole.CANDIDATE:
            CandidateProfile.objects.get_or_create(user=instance)
        elif instance.role == UserRole.EMPLOYER:
            EmployerProfile.objects.get_or_create(user=instance)
