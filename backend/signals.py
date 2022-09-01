from django.db.models.signals import pre_delete
from django.dispatch import receiver
from backend.models import ServiceUser, Annotation

@receiver(pre_delete, sender=ServiceUser)
def user_delete_cleanup(sender, **kwargs):
    """ Perform cleanup when a user is deleted"""

    delete_user = kwargs["instance"]

    # Remove all pending annotations
    pending_annotations = delete_user.annotations.filter(status=Annotation.PENDING)
    for pending in pending_annotations:
        pending.delete()
