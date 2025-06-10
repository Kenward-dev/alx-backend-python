from django.views import View
from .models import Message
from django.contrib.auth.models import get_user_model
from django.http import JsonResponse

User = get_user_model()

class MessageDeleteView(View):
    """
    View to handle the deletion of a message.
    """
    def post(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id, receiver=request.user)
            message.delete()
            return JsonResponse({'status': 'success', 'message': 'Message deleted successfully.'}, status=204)
        except Message.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Message not found.'}, status=404)