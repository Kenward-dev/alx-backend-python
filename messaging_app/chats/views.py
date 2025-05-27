from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for listing conversations and creating new ones."""
    
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return conversations where the authenticated user is a participant."""
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants').order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        """Create a new conversation with participants."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        participant_ids = request.data.get('participant_ids', [])
        if str(request.user.user_id) not in [str(pid) for pid in participant_ids]:
            participant_ids.append(request.user.user_id)
        
        conversation = Conversation.objects.create()
        participants = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(participants)
        
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for listing messages and sending new ones."""
    
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return messages from conversations where user is a participant."""
        user_conversations = Conversation.objects.filter(
            participants=self.request.user
        ).values_list('conversation_id', flat=True)
        
        return Message.objects.filter(
            conversation__conversation_id__in=user_conversations
        ).select_related('sender', 'conversation').order_by('-sent_at')
    
    def create(self, request, *args, **kwargs):
        """Send a new message to an existing conversation."""
        data = request.data.copy()
        data['sender_id'] = request.user.user_id
        
        conversation_id = data.get('conversation_id')
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            if not conversation.participants.filter(user_id=request.user.user_id).exists():
                return Response(
                    {'error': 'You are not a participant in this conversation.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        