from django.contrib import admin
from .models import Chat, ChatParticipant, Message

# Register your models here.
admin.site.register(Chat)
admin.site.register(ChatParticipant)
admin.site.register(Message)
