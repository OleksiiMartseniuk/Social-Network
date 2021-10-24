from django.db import models
from django.conf import settings
from base.services import get_path_upload_avatar


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to=get_path_upload_avatar, blank=True, null=True)

    def __str__(self):
        return self.user.username

