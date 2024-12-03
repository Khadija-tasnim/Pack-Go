from django.urls import path
from .import views

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('create/', views.create_tour, name='create_tour'),
    path('<int:pk>/', views.tour_detail, name='tour_detail'),
    path('<int:pk>/edit/', views.update_tour, name='update_tour'),
    path('<int:pk>/delete/', views.delete_tour, name='delete_tour'),
    path('order/history/', views.order_history, name='order_history'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:tour_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/place_order/', views.place_order, name='place_order'),
    path('order/detail/<int:order_id>/', views.order_detail, name='order_detail'),

]
