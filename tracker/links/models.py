from django.db import models

class Link(models.Model):
    title = models.CharField(max_length=200, unique=True)
    url = models.URLField(max_length=2000)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

class Click(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    date = models.DateTimeField(auto_now_add=True)
