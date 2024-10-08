from django.db import models

class AccessRecord(models.Model):
    access_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=50)
    urls = models.TextField()
    os_name = models.CharField(max_length=50)
    os_version = models.CharField(max_length=50)
    browser_name = models.CharField(max_length=50)
    browser_version = models.CharField(max_length=50)

    def __str__(self):
        return f"Access Record - {self.access_time}"
