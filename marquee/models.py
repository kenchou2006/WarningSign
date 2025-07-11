from django.db import models

class MarqueeMessage(models.Model):
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

class SignOnMessage(models.Model):
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

class SignOffMessage(models.Model):
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

class MarqueeSettings(models.Model):
    auto_message = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
