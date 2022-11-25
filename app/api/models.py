from django.db import models

class Plant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=360, null=True, blank=True)
    def __str__(self):
        return f'{self.name}'
