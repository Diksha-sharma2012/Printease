from django.contrib import admin
from .models import FilesUpload, Order
from django.contrib.auth.models import User

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ["name"]

class UserAdmin(admin.ModelAdmin):
    list_display = ["email"]


admin.site.register(FilesUpload)
admin.site.register(Order,OrderAdmin)
