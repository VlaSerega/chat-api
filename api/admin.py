from django.contrib import admin

from api.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(ConversationParticipants)
admin.site.register(Contacts)
