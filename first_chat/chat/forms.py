from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from chat.models import Chat, Invite
from regist.models import Profile

class InvateForm(forms.Form):

    username = forms.CharField(max_length=150)

    def clean_username(self):
        username = self.cleaned_data['username']
        r = User.objects.filter(username=username)
        if not r.count():
            raise ValidationError("Данного пользователя не существует")
        return username

    def save(self, request, chat_id):
        invite = Invite()
        invite.chat = get_object_or_404(Chat, pk = chat_id)
        invite.recipient = get_object_or_404(Profile, user=get_object_or_404(User, username=self.cleaned_data['username']))
        invite.sender = get_object_or_404(Profile, user=request.user)
        invite.save()

        return invite
