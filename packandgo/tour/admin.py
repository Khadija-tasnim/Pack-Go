from django.contrib import admin
from .models import TourDestinations, TourImage

admin.site.register(TourDestinations)
admin.site.register(TourImage)

from django.contrib import admin
from .models import  Cart, CartItem, Order, OrderItem

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)