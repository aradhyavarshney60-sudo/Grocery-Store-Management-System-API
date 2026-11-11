from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('Customer', 'Customer'),
        ('Admin', 'Admin'),
        ('DeliveryStaff', 'Delivery Staff'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Customer')

    def save(self, *args, **kwargs):
        if self.role == 'Admin':
            self.is_staff = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"


class GroceryItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    expiry_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Dispatched', 'Dispatched'),
        ('Delivered', 'Delivered'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    delivery_address = models.TextField()
    payment_method = models.CharField(max_length=50, default='Cash on Delivery')
    payment_status = models.CharField(max_length=50, default='Unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(GroceryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.item.name} for Order #{self.order.id}"