from django.db import models

class GlobalMessage(models.Model):
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)