from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from ckeditor.fields import RichTextField

class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def profile(self):
        profile = Profile.objects.get(user=self)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000)
    bio = models.TextField()
    image = models.ImageField(upload_to="profile-photos", default="default.jpg", blank=True)
    role = models.CharField(max_length = 100)
    verified = models.BooleanField(default=False)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
 
class Blogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    content = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    
    
    def __str__(self):
        return self.title[:30]

class Comment(models.Model):
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'

class TutorialName(models.Model):
    tutorialName = models.CharField(max_length=1000)
    tutorialContent = models.TextField()
    tutorialImage = models.ImageField(upload_to='Tutorials')
    def __str__(self):
        return self.tutorialName

class TutorialPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_title = models.CharField(max_length=100)
    post_content = RichTextField()
    post_file = models.FileField()
    tutorialName = models.ForeignKey(TutorialName, on_delete=models.CASCADE)   
    post_video = models.URLField()

    def __str__(self):
        return self.post_title
    


class Meme(models.Model):
    description = models.CharField(max_length=1100)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    images = models.FileField(upload_to='memes', default=1)

    def __str__(self):
        return self.description[:30]


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    subject = models.CharField(max_length=20)
    message = models.TextField(max_length=40)
    
    def __str__(self):
        return self.name