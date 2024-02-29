from django.db import models

# Create your models here.
import datetime

from django.db import models
# from django.contrib.auth import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Post(models.Model):

    title = models.CharField(max_length=255, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(null=True)
    # date_published = models.DateTimeField(default=timezone.now())
    date_published = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     if not self.date_published:
    #         self.date_published = timezone.now()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}-{self.author}-{self.date_published}'


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.created_at}'


class Contact(models.Model):

    name = models.CharField(max_length=255, null=True)
    contact_number = models.CharField(max_length=120, null=True)
    email_id = models.EmailField()
    body = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}-{self.contact_number}-{self.email_id}'



