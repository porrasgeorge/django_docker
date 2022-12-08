from django.db import models
#from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import datetime as dt



class Plant(models.Model):
    name = models.CharField(max_length=100, unique=True, default="")
    description = models.TextField(max_length=360, null=True, blank=True)
    ##image = models.FileField(default="")
    def __str__(self):
        return f'{self.name}'

class Generator(models.Model):
    plant = models.ForeignKey(Plant, related_name='generators', on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.plant} - {self.name}'
    class Meta:
        unique_together = ('plant', 'name')
        index_together = ['plant', 'name']

class ScadaPoint(models.Model):
    scada_pid = models.IntegerField(unique=True)
    generator = models.ForeignKey(Generator, related_name='scada_points', on_delete=models.PROTECT, default="")
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=360, null=True, blank=True)
    out_value = models.IntegerField(null=False, default=0)
    def __str__(self):
        return f'{self.generator} - {self.name} ({self.scada_pid})'

class Priority(models.Model):
    level = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.name} ({self.level})'
    class Meta:
        verbose_name_plural = "Priorities"

class Alarm(models.Model):
    scada_point = models.ForeignKey(ScadaPoint, related_name='alarms', on_delete=models.PROTECT, default="")
    priority = models.ForeignKey(Priority, related_name='alarms', on_delete=models.PROTECT, default="")
    date_time = models.DateTimeField(null=False, default=timezone.now)
    status = models.BooleanField(null=False, default=0)
    def __str__(self):
        return f'{"Entrada" if self.status else "Salida"}: {self.scada_point} - {self.date_time}'
    
