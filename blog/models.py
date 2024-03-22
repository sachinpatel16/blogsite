from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
# class User_detail(AbstractUser):
#     user_pic = models.FileField(upload_to='user_pic/',null=True,default=None)

class Category(models.Model):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    content=models.TextField()
    put_date = models.DateTimeField(auto_now_add=True)
    auther = models.ForeignKey(User,on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    
    def __str__(self):
        return self.title

class Coment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_coment')
    commenter = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.commenter.username} on {self.post.title}'

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Dislike(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Multimedia(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_pic')
    file = models.FileField(upload_to='post_pic/',null=None)