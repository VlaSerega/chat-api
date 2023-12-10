from django.db import transaction, IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from api.models import Conversation, ConversationParticipants

class ConversationSerializer(serializers.ModelSerializer):
    participant_id = serializers.IntegerField(write_only=True)
    owner = serializers.IntegerField(read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'title', 'conversation_type', 'owner', 'participant_id')

    def create(self, validated_data):
        with transaction.atomic():
            participant_id = validated_data.pop('participant_id')
            conversation = Conversation.objects.create(**validated_data)
            ConversationParticipants.objects.create(conversation_id=conversation, user_id=self.context['request'].user)
            ConversationParticipants.objects.create(conversation_id=conversation, user_id=participant_id)

        return conversation


class AddParticipantsSerializer(serializers.Serializer):
    conversation_id = serializers.IntegerField()
    participants = serializers.ListSerializer(child=serializers.IntegerField())

    default_error_messages = {
        'bad_conversation': 'Такого диалога не существует.',
        'conversation_one_to_one': 'В личный диалог нельзя добавить участников.',
        'user_in_conversation': 'Один или более людей уже состоят в группе.'
    }

    def create(self, validated_data):
        conversation_id = validated_data.pop('conversation_id')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            if conversation.conversation_type == Conversation.Type.ONE_TO_ONE:
                self.fail('conversation_one_to_one')
        except NotFound:
            self.fail('bad_conversation')

        participants = validated_data.pop('participants')
        try:
            ConversationParticipants.objects.bulk_create(
                [ConversationParticipants(conversation_id=conversation_id, user_id=p) for p in participants])
        except IntegrityError as e:
            if e.pgcode == 23505:
                self.fail('user_in_conversation')
