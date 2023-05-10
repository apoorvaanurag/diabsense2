from django.db import models
import random
from django.utils import timezone

from datetime import datetime, timedelta
from django.core.validators import validate_image_file_extension


class UploadImage(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images", validators=[validate_image_file_extension])

    def __str__(self):
        pass
