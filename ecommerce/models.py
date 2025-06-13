from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name
    
    class CartItem(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        product = models.ForeignKey('Product', on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField()

    class Order(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        ordered_at = models.DateTimeField(auto_now_add=True)

    class OrderItem (models.Model):
        order = models.ForeignKey('Order', related_name = 'items', on_delete=models.CASCADE)
        product = models.ForeignKey('Product', on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField()

