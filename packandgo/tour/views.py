from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import TourDestinations, TourImage
from .forms import TourDestinationForm, TourImageForm
from django.contrib.auth.decorators import login_required
from .models import TourDestinations, Cart, CartItem, Order, OrderItem



def create_tour(request):
    if request.method == 'POST':
        form = TourDestinationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tour_list')
    else:
        form = TourDestinationForm()
    return render(request, 'tour/create_tour.html', {'form': form})


def tour_list(request):
    tours = TourDestinations.objects.all()
    return render(request, 'tour/tour_list.html', {'tours': tours})


from django.shortcuts import render, get_object_or_404, redirect
from .models import TourDestinations, TourImage
from .forms import TourImageForm


def tour_detail(request, pk):
    tour = get_object_or_404(TourDestinations, pk=pk)

    if request.method == 'POST':
        form = TourImageForm(request.POST, request.FILES)
        if form.is_valid():

            image = form.save(commit=False)
            image.tour = tour
            image.save()

            return redirect('tour_detail', pk=tour.pk)
    else:
        form = TourImageForm()

    return render(request, 'tour/tour_detail.html', {'tour': tour, 'form': form})


def update_tour(request, pk):
    tour = get_object_or_404(TourDestinations, pk=pk)
    if request.method == 'POST':
        form = TourDestinationForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('tour/tour_detail', pk=tour.pk)
    else:
        form = TourDestinationForm(instance=tour)
    return render(request, 'tour/update_tour.html', {'form': form})


def delete_tour(request, pk):
    tour = get_object_or_404(TourDestinations, pk=pk)
    if request.method == 'POST':
        tour.delete()
        return redirect('tour/tour_list')
    return render(request, 'tour/delete_tour.html', {'tour': tour})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    total_price = sum(item.total_price() for item in cart.items.all())
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})

@login_required
def add_to_cart(request, tour_id):
    tour = get_object_or_404(TourDestinations, id=tour_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, tour=tour)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_view')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if 'quantity' in request.POST:
        cart_item.quantity = int(request.POST['quantity'])
        cart_item.save()
    return redirect('cart_view')

@login_required
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        return redirect('cart_view')

    total_price = sum(item.total_price() for item in cart.items.all())
    order = Order.objects.create(user=request.user, total_price=total_price)
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            tour=item.tour,
            quantity=item.quantity,
            price_per_day=item.tour.price_per_day
        )
    cart.items.all().delete()  # Clear cart after placing order
    return render(request, 'order_confirmation.html', {'order': order})

