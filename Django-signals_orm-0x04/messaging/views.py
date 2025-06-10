from django.contrib.auth.models import get_user_model
from django.http import JsonResponse

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