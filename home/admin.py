from django.contrib import admin
from .models import Blog

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['user','title','short_description','main_image']
    # list_display = [field.name for field in Blog._meta.fields]
    