from django.db import models
from django.contrib.auth.models import User


class Wiki(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    summary = models.CharField(max_length=500)
    image = models.URLField(null=True)
    query = models.CharField(max_length=200)
    user = models.ManyToManyField(User)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ["-image", "-id"]

    