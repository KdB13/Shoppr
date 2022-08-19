from django.contrib import admin
from . import models

class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "vendor", "price", "stock", "photo", "id"]


class VendorAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "address", "id"]

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Vendor, VendorAdmin)