from django.db import models
from django.contrib.auth import get_user_model
import uuid     # generate unique id
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=30, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)        # Foreign Key
    id_user = models.IntegerField()
    bio = models.TextField(blank=True, max_length=150)
    profileimg = models.ImageField(upload_to = 'profile_images', default = 'profile.jpg')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = "Profile"
    

class Post(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)         # Universal Unique Identifier
    user = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = "post_images")
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user
    
    class Meta:
        db_table = "Post"
        
class LikePost(models.Model):
    post_id = models.CharField(max_length = 500)
    username = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.username
    
class FollowersCount(models.Model):
    follower = models.CharField(max_length = 100)
    user = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.user