from django.contrib.auth.models import get_user_model
from django.http import JsonResponse
from .models import Message

User = get_user_model()

def delete_user(request, user_id):
    """
    View to delete a user and all their related messages.
    """
    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        return JsonResponse({'status': 'success', 'message': 'User and related messages deleted successfully.'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)

def get_threaded_messages(request):
    """
    View to get all threaded messages for the user
    """
    return Message.objects.filter(
        sender=request.user,
        parent_message=None
    ).select_related('sender', 'receiver').prefetch_related('replies__sender', 'replies__receiver').order_by('-timestamp')