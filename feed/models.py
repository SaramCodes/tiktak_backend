from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

file_validator = FileExtensionValidator(['mp4','mov'], "Only mp4 and mov files are allowed")


class Post(models.Model):
    title = models.CharField(max_length=500)
    video = models.FileField(upload_to="videos", validators=[file_validator])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)



class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)