from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pictures", default="profile_pictures/default.jpg")
    description = models.TextField(blank=True)
    followers = models.ManyToManyField(User, related_name="followers", blank=True)
    following = models.ManyToManyField(User, related_name="following", blank=True)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
