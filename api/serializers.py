from rest_framework import serializers
from django.db import transaction, IntegrityError
from api.models import User, Conversation, ConversationParticipants


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'last_name', 'date_joined', )


class UserSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'last_name')


class MyConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ('id', 'title', 'owner')


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ('title', 'conversation_type')

    def create(self, validated_data):
        with transaction.atomic():
            conversation = Conversation.objects.create_user(**validated_data)
            ConversationParticipants.objects.create(conversation_id=conversation, user_id=self.context['request'].user)

        return conversation
