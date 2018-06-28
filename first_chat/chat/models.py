from django.db import models
from regist.models import Profile

class Chat(models.Model):
    users = models.ManyToManyField(Profile)
    admin = models.ForeignKey(Profile, related_name='admin', on_delete=models.SET_NULL, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='image/%Y/%m/%d', default='/img/user-png-icon-male-user-icon-512.png', blank=True, null=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Invite(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, related_name='sender', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.chat.name
