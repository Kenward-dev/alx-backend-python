from django.views import View
from django.contrib.auth.models import get_user_model
from django.http import JsonResponse

User = get_user_model()

class DeleteUser(View):
    """
    View to delete a user and all their related messages.
    """
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'status': 'success', 'message': 'User deleted successfully.'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)