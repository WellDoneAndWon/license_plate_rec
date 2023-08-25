from django.db import models


class UploadedContent(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True)
    video = models.FileField(upload_to='videos/', null=True)

    def __str__(self):
        return self.title
