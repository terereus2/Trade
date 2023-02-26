from django.db import models
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime


# Create your models here.

class Blog(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    date = models.DateField()
    text = models.TextField(max_length=2000)


class Article(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=5000)
    date = models.DateField()
    post_pos = models.IntegerField(default=0)
    post_neg = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.text


class UserVote(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    vote_type = models.CharField(max_length=10)


class Contact(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=250)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=1000)
