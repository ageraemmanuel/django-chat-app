from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Chat
from .forms import UserCreationForm


def home(req):
  messages = messages = Message.objects.filter(sender=req.user)

  context = {'messages': messages}

  if req.method == 'POST':
    chat, create = Chat.objects.get()
    message = req.POST.get('message')
    user = req.user.username
    res = Messages.object.create(
      sender=user,
      chat=chat,
      content=message
    )     
    print(res)

  return render(req, 'mainapp/index.html', context)

  # Register views
def register(req):
  form = UserCreationForm()
  context = {'form': form}

  if req.method == 'POST':
    form = UserCreationForm(req.POST)

    if form.is_valid:
      req.authenticate()
      form.save()
  
  return render(req, 'mainapp/register.html', context)

def chatroom(req, pk):
  message = Message.objects.get(id=pk)
  context = {'message': message}
  return render(req, 'mainapp/chatroom.html', context)