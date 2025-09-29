from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponse
from .models import Chat, User
from .forms import UserCreationForm


def home(req):
  chat = Chat.objects.all()
  users = User.objects.all()
  context = {'users': users, 'user': req.user}
  return render(req, 'mainapp/index.html', context)

  # Register views
def register(req):
  if req.method == 'POST':
    form = UserCreationForm(req.POST)
    if form.is_valid():
      user = form.save()
      login(req, user)
      return redirect('home')
  else:
    form = UserCreationForm()
    
  context = {'form': form}
  return render(req, 'mainapp/register.html', context)

def chatroom(req, pk):
  message = Message.objects.get(id=pk)
  context = {'message': message}
  return render(req, 'mainapp/chatroom.html', context)