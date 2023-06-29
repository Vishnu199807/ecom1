from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Categories(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name


class Products(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images", null=True)
    price = models.PositiveBigIntegerField()
    description = models.CharField(max_length=250, null=True)
    quantity = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.product_name

class Carts(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    options = (
        ("in-cart", "in-cart"),
        ("order-placed", "order-placed"),
        ("cancelled", "cancelled")
    )
    status = models.CharField(max_length=150, choices=options, default="in-cart")
    qty = models.PositiveIntegerField(default=1)


class Orders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    options = (
        ("order-placed", "order-placed"),
        ("dispatched", "dispatched"),
        ("in-transit", "in-transit"),
        ("delivered", "delivered"),
        ("cancelled", "cancelled")
    )
    status = models.CharField(max_length=150, choices=options, default="order-placed")
    delivery_address = models.CharField(max_length=200, null=True)
    expected_delivery_date = models.DateField(null=True)


class Reviews(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.CharField(max_length=300)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comments

    # super user>> Username=xyz,Password=Password@123