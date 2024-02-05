from django.urls import reverse_lazy
from .models import TaskGroup, Invitation


def create_invitation(request, group_id):
    group = TaskGroup.objects.get(id=group_id)
    sender = request.user
    invitation = Invitation.objects.create(
        group=group,
        sender=sender
    )
    return invitation

def get_invitation_link(request, invitation):
    link = request.build_absolute_uri(reverse_lazy("groups:accept_invitation", args=[invitation.token]))
    return link

