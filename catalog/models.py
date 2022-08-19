from datetime import date

from django.db import models
from django.urls import reverse

# Create your models here.
class User(models.Model):
    ERROR_EMAIL_EXISTS = "A user with this email already exists."

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(unique=True, error_messages={"unique": ERROR_EMAIL_EXISTS})
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Vendor(models.Model):
    ERROR_EMAIL_EXISTS = "A user with this email already exists."

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, error_messages={"unique": ERROR_EMAIL_EXISTS})
    password = models.CharField(max_length=128)
    address = models.TextField(default="")

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True)
    price = models.FloatField()
    stock = models.IntegerField(default=0)
    photo = models.ImageField(upload_to="images/products", blank=True, null=True)

    def __str__(self):
        return self.title
    

    def format_price(self):
        return f"₹{self.price:,.0f}"
    

    def get_absolute_url(self):
        return reverse("catalog:product-details", args=[self.id])


    def get_edit_url(self):
        return reverse("catalog:vendors-edit-product", args=[self.id])


    def get_delete_url(self):
        return reverse("catalog:vendors-delete-product", args=[self.id])