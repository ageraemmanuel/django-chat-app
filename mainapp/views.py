from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponse
from .models import Chat, User, FriendRequest, Friend
from .forms import UserCreationForm
from django.contrib import messages

def home(req):
  users = User.objects.exclude(id=req.user.id)
  context = {
    'users': users, 
    'user': req.user, 
    'title': 'Home | Selam'
  }

  return render(req, 'mainapp/index.html', context)

  # Register views
def register(req):
  if req.method == 'POST':
    form = UserCreationForm(req.POST, req.FILES)
    if form.is_valid():
      user = form.save()
      login(req, user)
      return redirect('home')
  else:
    form = UserCreationForm()
    
  context = {
    'form': form,
    'title': 'Sign Up | Selam'
    }
  return render(req, 'mainapp/register.html', context)

from django.shortcuts import render, get_object_or_404

def user_profile(req, pk):
  profile_user = get_object_or_404(User, id=pk)
  friend_requests = FriendRequest.objects.filter(receiver=profile_user, is_accepted=False)
  friends = Friend.objects.filter(user=profile_user)

  context = {
    'user': profile_user,
    'friend_requests': friend_requests,
    'friends': friends,
    'title': f"{profile_user.username} | Selam"
  }
  return render(req, 'mainapp/profile.html', context)

def follow(req, pk):
  if req.user.id != pk:
    user = User.objects.get(id=pk)
    if user:
      FriendRequest.objects.create(
        sender=req.user,
        receiver=user
      )      
      messages.success(req, "Friend Request sent successfully!")
      return redirect('home')
    else:
      messages.error(req, "User does not exist!")
      return redirect('home')
  else:
    messages.error(req, "Can't follow yourself!")
    return redirect('home')

def approve_request(req, pk):
  user = User.objects.get(id=pk)
  if user:
    Friend.objects.create(
      user=req.user,
      friend=user
    ) 
    FriendRequest.objects.update(
        is_accepted=True
      )     
    messages.success(req, "Friend Request sent successfully!")
    return redirect('user_profile', pk)
  else:
    messages.error(req, "User does not exist!")
    return redirect('user_profile', pk)