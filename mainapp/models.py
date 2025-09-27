from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat(models.Model):
  """
  chat can either be private or a group chat
  """
  # name of the chat (group name) or( user1+user2 or null for private chat)
  name  = models.CharField(max_length=100, blank=True, null=True)
  chat_type = models.CharField(max_length=20) #private or group
  participants = models.ManyToManyField(User, related_name='chats', through='ChatParticipant')

  def __str__(self):
    return self.name or f"Chat {self.id}"

class ChatParticipant(models.Model):
  """
  This model will connect users to the chat model
  """
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
  joined_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('user', 'chat') #Ensures the user join chat only once

class Message(models.Model):
  """
  This represent the message sent within a chat
  """

  #links athe message to a specific conversion
  chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
  sender = models.ForeignKey(User, related_name='sent_message', on_delete=models.CASCADE)
  content = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['timestamp'] #how to arrange the data when querry 

  def __str__(self):
    return f"message from {self.sender.username} in {self.chat}"