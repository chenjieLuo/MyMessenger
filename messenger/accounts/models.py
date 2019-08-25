from django.db import models
from django.contrib.auth.models import User
from django import forms


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        person1, created = cls.objects.get_or_create(current_user=current_user)
        person1.users.add(new_friend)
        person2, created = cls.objects.get_or_create(current_user=new_friend)
        person2.users.add(current_user)

    @classmethod
    def break_friend(cls, current_user, old_friend):
        person1, created = cls.objects.get_or_create(current_user=current_user)
        person1.users.remove(old_friend)
        person2, created = cls.objects.get_or_create(current_user=old_friend)
        person2.users.remove(current_user)


class Post(models.Model):
    post = models.CharField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
