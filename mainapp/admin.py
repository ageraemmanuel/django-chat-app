from django.contrib import admin
from .models import Chat, Friend, FriendRequest, User

# Register your models here.
admin.site.register(Chat)
admin.site.register(Friend)
admin.site.register(FriendRequest)
admin.site.register(User)
