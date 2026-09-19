import logging
from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Notification

logger = logging.getLogger('apps')
User = get_user_model()

@shared_task(name="send_application_status_notification")
def send_application_status_notification(user_id, job_title, new_status):
    """
    Celery task to send asynchronous status update notifications to candidates.
    """
    try:
        user = User.objects.get(id=user_id)
        title = f"Application Status Update: {job_title}"
        message = f"Your application status for '{job_title}' has been updated to '{new_status}'."

        notification = Notification.objects.create(
            user=user,
            title=title,
            message=message
        )
        logger.info(f"Notification {notification.id} created for user {user.username}")
        return f"Notification created for user {user_id}"
    except User.DoesNotExist:
        logger.error(f"Failed to create notification. User ID {user_id} not found.")
        return f"User {user_id} not found"
    except Exception as e:
        logger.error(f"Error creating notification task: {str(e)}", exc_info=True)
        raise e
