import uuid
from allauth.account.signals import user_logged_in, user_signed_up
from django.dispatch import receiver

from .models import Invitation

@receiver(user_logged_in)
@receiver(user_signed_up)
def process_invitation(sender, **kwargs):
    request = kwargs.get("request")
    user = kwargs.get("user")
    token = request.session.pop("invitation_token", None)
    if token:
        token = uuid.UUID(token)
        try:
            invitation = Invitation.objects.get(token=token, accepted=False)
            invitation.group.members.add(user)
            invitation.accepted = True
            invitation.save()
        except Invitation.DoesNotExist:
            pass
