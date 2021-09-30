from django.db import models

import uuid

from django.db.models.fields.related import ForeignKey

from account.models import User
# Create your models here.

class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.ImageField(upload_to="user_uploaded")
    caption = models.TextField(null=True, blank=True, max_length=2200)
    allow_comments = models.BooleanField(default=True, help_text="Allow people to comment on this post?")
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.user} | {self.id}')

    class Meta:
        ordering = ['-date_published']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=2200)

    def __str__(self):
        return str(f'{self.user} | {self.comment}')

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(f'{self.user} | {self.post} ')

class SavedPost(models.Model):
    post = ForeignKey(Post, on_delete=models.CASCADE)
    user = ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(f'{self.user} | {self.post}')

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User_who_follow', help_text='This user is following the user below. |Increased a following|')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User_being_followed', help_text='This user is being followed. |Increased a follower|')

    def __str__(self):
        return str(f'{self.user} | Follows | {self.following}')