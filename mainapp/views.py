from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from .models import Chat, User, FriendRequest, Friend
from .forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError



# HOME VIEW

def home(request):

  if request.user.is_authenticated:
    current_user = request.user

    friend_ids = Friend.objects.filter(user=current_user).values_list('friend_id', flat=True)

    pending_req = FriendRequest.objects.filter(receiver=current_user, is_accepted=False)

    pending_request_ids = FriendRequest.objects.filter(
        receiver=current_user
    ).values_list('sender_id', flat=True)

    # Exclude: self, friends, and users who sent the current user a friend request
    users = User.objects.exclude(id=current_user.id)\
                        .exclude(id__in=friend_ids)\
                        .exclude(id__in=pending_request_ids)

    context = {
        'users': users,
        'pending_req': pending_req,
        'title': 'Home | Selam'
    }
    return render(request, 'mainapp/index.html', context)

  else:
    context = {'users': User.objects.all(), 'title': 'Home | Selam'}
    return render(request, 'mainapp/index.html', context)


# REGISTER VIEW
def register(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST, request.FILES)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
  else:
    form = UserCreationForm()
    
  context = {
    'form': form,
    'title': 'Sign Up | Selam'
    }
  return render(request, 'mainapp/register.html', context)

#LOGIN VIEW
def login_view(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)

    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(request, username=username, password=password)

      if user is not None:
        login(request, user)
        messages.success(request, f"Welcome, {username}!")
        nexturl = request.POST.get('next') or request.GET.get('next') or 'home'
        return redirect(nexturl)
      else:
        messages.warn(request, "Invalid username or password.")
    else:
      messages.warn(request, "Invalid username or password.")
  else:
    next_url = request.GET.get('next', '/')
    form = AuthenticationForm()
    context = {'form': form, 'next_url': next_url }
  return render(request, 'mainapp/register.html', context)

# LOGOUT VIEW
@login_required
def logout_view(request):
  logout(request)
  messages.info(request, "You have been logged out.")
  return redirect('home')

# USER PROFILE VIEW
@login_required
def user_profile(request, pk):
  profile_user = get_object_or_404(User, id=pk)
  friend_requests = FriendRequest.objects.filter(receiver=profile_user, is_accepted=False)
  friends = Friend.objects.filter(user=profile_user)

  context = {
    'user': profile_user,
    'friend_requests': friend_requests,
    'friends': friends,
    'title': f"{profile_user.username} | Selam"
  }
  return render(request, 'mainapp/profile.html', context)

# FOLLOW ACTION VIEW
def follow(request, pk):
  if not request.user.is_authenticated:
    return redirect('login')

  if request.user.id != pk:
    user = User.objects.get(id=pk)
    if user:
      FriendRequest.objects.create(
        sender=request.user,
        receiver=user
      )      
      messages.success(request, "Friend Request sent successfully!")
      return redirect('home')
    else:
      messages.error(request, "User does not exist!")
      return redirect('home')
  else:
    messages.error(request, "Can't follow yourself!")
    return redirect('home')

# APPROVE fOLLOW VIEW
@login_required
def approve_request(request, pk):
  sender = get_object_or_404(User, id=pk)

  if sender.id == request.user.id:
    messages.error(request, "You can't approve your own request.")
    return redirect('user_profile', pk)

  friend_request = FriendRequest.objects.filter(sender=sender, receiver=request.user, is_accepted=False).first()

  if not friend_request:
    messages.error(request, "No pending request found.")
    return redirect('user_profile', pk)

  # Mark request as accepted
  friend_request.is_accepted = True
  friend_request.save()

  try:
    Friend.objects.create(user=request.user, friend=sender)
  except IntegrityError:
    pass

  try:
    Friend.objects.create(user=sender, friend=request.user)
  except IntegrityError:
    pass

  messages.success(request, "Friend request accepted.")
  return redirect('user_profile', pk)
