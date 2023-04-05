from django.db import models
import random
from django.utils import timezone
# fix this 'datetime.datetime' has no attribute 'timedelta'
from datetime import datetime, timedelta


class UploadImage(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    # add 5.5 hours to datetimefield
    image = models.ImageField(upload_to="images")

    def __str__(self):
        pass
