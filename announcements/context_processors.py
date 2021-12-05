from .models import Announcement


def announcement_context_processor(request):
    """
    Adds the active announcements to the context
    """
    return {
        'announcements': Announcement.objects.filter(display=True)
    }