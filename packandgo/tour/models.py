from django.db import models
from django.contrib.auth.models import User

class TourDestinations(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class TourImage(models.Model):
    tour = models.ForeignKey(TourDestinations, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='tour_images/')

    def __str__(self):
        return f"Image for {self.tour.name}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    tour = models.ForeignKey(TourDestinations, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.tour.name}"

    def total_price(self):
        return self.quantity * self.tour.price_per_day

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    tour = models.ForeignKey(TourDestinations, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.tour.name} in Order {self.order.id}"
