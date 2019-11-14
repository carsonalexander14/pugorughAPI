from django.contrib.auth.models import User
from django.db import models


from django.db.models.signals import post_save
from django.dispatch import receiver


class Dog(models.Model):
    name = models.CharField(max_length=255, blank=True)
    image_filename = models.CharField(max_length=255, blank=True)
    breed = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(blank=True, default=1)
    gender = models.CharField(max_length=1, blank=True)
    size = models.CharField(max_length=2, blank=True)


class UserDog(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    dog = models.ForeignKey(to=Dog, on_delete=models.CASCADE)
    status = models.CharField(max_length=1)


class UserPref(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    age = models.CharField(max_length=7, blank=True)
    gender = models.CharField(max_length=3, blank=True)
    size = models.CharField(max_length=8, blank=True)


@receiver(post_save, sender=User)
def after_created(sender, instance, created, ** kwargs):
    if created:
        UserPref.objects.create(
            user=instance,
        )
