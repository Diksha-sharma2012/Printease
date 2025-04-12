from django.contrib import admin
from .models import FilesUpload, Order, OrderBillModel, OrderLetterModel


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ["name"]

class UserAdmin(admin.ModelAdmin):
    list_display = ["email"]

class OrderBillAdmin(admin.ModelAdmin):
    list_display = ["company_name"]

class OrderLetterAdmin(admin.ModelAdmin):
    list_display = ["company_name"]

admin.site.register(OrderBillModel,OrderBillAdmin)
admin.site.register(FilesUpload)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderLetterModel,OrderLetterAdmin)
