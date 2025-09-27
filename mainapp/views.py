from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Message, Chat
from .forms import MessageForm


def home(req):
  messages = Message.objects.all()
  print(messages)
  form = MessageForm()
  print(form)
  if req.method=='POST':
    message=req.POST.get('message')
    username=req.POST.get('username')
    Message.objects.create(
      chat=messages.chat.name,
      sender=username,
      content=message
    )

  data = {'data': messages, 'form': form}
  return render(req, 'mainapp/index.html', data )
#
def chatroom(req, pk):
  message=Message.objects.all()
  return render(req, "mainapp/chatroom.html", {'customer': message})

# def sendchat(request):
#   message = None
#   name = None
#   if request.method == "POST":
#     form = MessageForm(request.POST)
#     print(form)
#     if form.is_valid():
#       form.save()
#     else:
#       print('invalid form')
#     return redirect('home')
#   else:
#     return redirect('chatroom')