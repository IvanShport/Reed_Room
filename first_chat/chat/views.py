from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from chat.models import Chat, Message, Invite
from regist.models import Profile
from chat.forms import InvateForm

@login_required
def index(request):
    chats = Chat.objects.filter(users__user = request.user, create_date__lte=timezone.now()).order_by('-create_date')
    invites = Invite.objects.filter(recipient__user = request.user)
    return render(request, 'chat/chat.html', {
        'invites': invites,
        'chats': chats,
    })

@login_required
def SendMessageView(request, pk):
    if request.method == 'POST':
        chat = get_object_or_404(Chat, pk = pk)
        text = request.POST.get('text')
        if text == '':
            return HttpResponseRedirect(reverse('chat:open_chat', args=(pk,)))
        message = Message()
        message.chat = chat
        message.text = text
        message.author = get_object_or_404(Profile, user = request.user)
        message.save()
    return HttpResponseRedirect(reverse('chat:open_chat', args=(pk,)))

@login_required
def OpenChatView(request, pk):
    form = InviteView(request, pk)
    chats = Chat.objects.filter(users__user=request.user, create_date__lte=timezone.now()).order_by('-create_date')
    invites = Invite.objects.filter(recipient__user=request.user)
    open_chat = get_object_or_404(Chat, pk = pk)
    return render(request, 'chat/chat.html', {
        'invites': invites,
        'form': form,
        'chats': chats,
        'open_chat': open_chat,
    })

def JoinView(request, pk):
    chat = get_object_or_404(Chat, pk = pk)
    chat.users.add(get_object_or_404(Profile, user=request.user))

    invite = Invite.objects.filter(chat__pk=pk)
    invite.delete()

    return HttpResponseRedirect(reverse('chat:open_chat', args=(pk,)))

def InviteView(request, pk):
    if request.method == 'POST':
        form = InvateForm(request.POST)
        if form.is_valid():
            form.save(request, pk)
            pass
    else:
        form = InvateForm()
    return form

@login_required
def CreateChatView(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name == '':
            return HttpResponseRedirect(reverse('chat:chat'))
        chat = Chat()
        chat.admin = get_object_or_404(Profile, user=request.user)
        chat.name = name
        chat.save()

        chat.users.add(get_object_or_404(Profile, user=request.user))
        chat.save()

    return HttpResponseRedirect(reverse('chat:open_chat', args=(chat.pk,)))