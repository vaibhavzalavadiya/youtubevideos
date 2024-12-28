from django.db import models

# Create your models here.
from django.db import models

class DownloadHistory(models.Model):
    video_url = models.URLField()
    download_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_url
