from django.contrib import admin
from .models import User


@admin.register(User)
class NameAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "city")
