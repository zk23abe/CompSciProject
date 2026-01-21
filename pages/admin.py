from django.contrib import admin

from django.contrib import admin
from .models import Student, Invoice

#manage tables in admin panel
admin.site.register(Student)
admin.site.register(Invoice)
admin.site.register(Lesson)
