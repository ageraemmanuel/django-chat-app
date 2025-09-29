from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  email = models.EmailField(unique=True)  # Make email unique
  dob = models.DateField(blank=True, null=True)
  avater = models.ImageField(upload_to='images/', default='', blank=True, null=True)
  phone_number = models.CharField(max_length=20, blank=True)
  bio = models.TextField(max_length=500, blank=True, null=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  USERNAME_FIELD = 'email' 
  REQUIRED_FIELDS = ['username', 'phone_number'] 
  
  def __str__(self):
    return self.email

class FriendRequest(models.Model):
  sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
  receiver = models.ForeignKey(User, related_name='recieved_requests', on_delete=models.CASCADE)
  is_accepted = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('sender', 'receiver') 

  def __str__(self):
    return f"You received a friend request from {self.sender}"

class Friend(models.Model):
  user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
  friend = models.ForeignKey(User, related_name='friends_with', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    unique_together = ('user', 'friend')

  def __str__(self):
    return f"{self.friend}"

class Chat(models.Model):
  sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
  receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  is_read = models.BooleanField(default=False)
  
  def __str__(self):
    return f"message from {self.sender} to {self.receiver}: {self.content[0:20]}"

class Post(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=100)
  descriptions = models.TextField(blank=True, null=True)
  imageurl = models.ImageField(upload_to='images/' ,blank=True, null=True)
  video = models.FileField(upload_to='videos/')

  def __str__(self):
    return self.title