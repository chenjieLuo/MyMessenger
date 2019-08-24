from django.db import models
from django.contrib.auth.models import User


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.users.add(new_friend)

    @classmethod
    def break_friend(cls, current_user, old_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.users.remove(old_friend)