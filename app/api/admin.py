from django.contrib import admin
from .models import Plant, Generator, ScadaPoint, Priority

admin.site.register(Plant)
admin.site.register(Generator)
admin.site.register(ScadaPoint)
admin.site.register(Priority)


