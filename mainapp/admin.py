from django.contrib import admin
from .models import Chat, Friends, FriendRequest

# Register your models here.
admin.site.register(Chat)
admin.site.register(Friends)
admin.site.register(FriendRequest)
