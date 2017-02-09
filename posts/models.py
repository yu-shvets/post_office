from django.db import models
from post_office.settings import AUTH_USER_MODEL

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
