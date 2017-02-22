from django.db import models
from post_office.settings import AUTH_USER_MODEL

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# Create your models here.


class Posts(models.Model):

    class Meta(object):
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-datetime']

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name="Title"
    )

    datetime = models.DateTimeField(
        auto_now_add=True
    )

    post = models.TextField(
        blank=False,
        verbose_name="Post"
    )

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}-{}".format(self.user, self.title)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
