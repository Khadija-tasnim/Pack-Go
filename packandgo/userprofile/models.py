
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg',upload_to="profile_pics/")
    full_name = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def _str_(self):
        return f'{self.user.username} Profile'
