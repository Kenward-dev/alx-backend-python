from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ['user_id', 'date_joined' 'last_login']

class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for the Conversation model."""
    
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the Message model."""
    
    sender = UserSerializer(read_only=True)
    conversation = ConversationSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']