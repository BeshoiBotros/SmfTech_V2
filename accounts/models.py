from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    
    gender_choices = (('Male', 'Male'), ('Female', 'Female'))

    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    image   = models.ImageField(upload_to='accounts/profiles/', default='default-user.jpg')
    address = models.CharField(max_length=255, null=True, blank=True)
    bio     = models.TextField(blank=True, null=True)
    gender  = models.CharField(null=True, blank=True, max_length=255, choices=gender_choices)
    
    def __str__(self) -> str:
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwarg):
    if created:
        Profile.objects.create(user=instance)


class ResetPasswordToken(models.Model):
    token = models.CharField(max_length=255)