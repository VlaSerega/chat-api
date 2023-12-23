from django.db import transaction, IntegrityError
from rest_framework import serializers

from api.models import Conversation, ConversationParticipants
from api.users.serializers import UserSmallSerializer


class ConversationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ('id', 'title', 'conversation_type')


class ConversationModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ('id', 'title', 'owner')


class ConversationCreateSerializer(serializers.ModelSerializer):
    participant_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'title', 'conversation_type', 'participant_id')

    def create(self, validated_data):
        with transaction.atomic():
            participant_id = validated_data.pop('participant_id')
            conversation = Conversation.objects.create(**validated_data)
            ConversationParticipants.objects.create(conversation=conversation, user=self.context['request'].user)
            ConversationParticipants.objects.create(conversation=conversation, user=participant_id)

        return conversation


class ConversationParticipantsSerializer(serializers.ModelSerializer):
    participants = serializers.ListSerializer(child=serializers.IntegerField(), write_only=True)
    user = UserSmallSerializer(read_only=True)

    default_error_messages = {
        'conversation_one_to_one': 'В личный диалог нельзя добавить участников.',
        'user_in_conversation': 'Один или более людей уже состоят в группе.'
    }

    class Meta:
        model = ConversationParticipants
        fields = ('user', 'participants')

    def create(self, validated_data):
        conversation = self.context['conversation']
        if conversation.conversation_type == Conversation.Type.ONE_TO_ONE:
            self.fail('conversation_one_to_one')

        participants = validated_data.pop('participants')
        try:
            return ConversationParticipants.objects.bulk_create(
                [ConversationParticipants(conversation=conversation, user=p) for p in participants])
        except IntegrityError as e:
            if e.pgcode == 23505:
                self.fail('user_in_conversation')
