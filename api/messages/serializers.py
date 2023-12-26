from rest_framework import serializers

from api.models import Message, ConversationParticipants


class MessageUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'text', 'owner', 'date')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'text', 'owner', 'date')


class MessageCreateSerializer(serializers.ModelSerializer):
    owner = serializers.IntegerField(read_only=True, source='owner_id')
    date = serializers.DateTimeField(read_only=True)

    default_error_messages = {
        'conversation_not_found': 'Вы не состоите в указанном диалоге или такого диалога не существует.'}

    class Meta:
        model = Message
        fields = ('id', 'text', 'owner', 'date', 'conversation')
        extra_kwargs = {'text': {'required': True}}

    def create(self, validated_data):
        user = self.context['request'].user
        conversation = validated_data.get('conversation')

        if not ConversationParticipants.objects.filter(user=user, conversation=conversation).exists():
            self.fail('conversation_not_found')

        return Message.objects.create(owner=user, **validated_data)
