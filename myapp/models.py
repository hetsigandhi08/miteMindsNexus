from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forgot_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add= True)

    
class UploadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_name = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)
    mites_count = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}'s Upload - {self.upload_date}"