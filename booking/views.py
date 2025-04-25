from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Show, Cart, BookingHistory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

class ShowListView(View):
    def get(self, request):
        shows = Show.objects.all()
        return render(request, 'booking/show_list.html', {'shows': shows})

    def post(self, request):
        match_id = request.POST.get('match_id')
        num_tickets = int(request.POST.get('num_tickets', 1))

        # Adding to cart using session
        cart = request.session.get('cart', {})
        if match_id in cart:
            cart[match_id] += num_tickets
        else:
            cart[match_id] = num_tickets
        request.session['cart'] = cart
        return redirect('show_list')


class RegisterView(View):
    def get(self, request):
        return render(request, 'booking/register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists.")
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('/')


class LoginView(View):
    def get(self, request):
        return render(request, 'booking/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        return HttpResponse("Invalid credentials")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')


class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        shows = Show.objects.filter(id__in=cart.keys())

        cart_items = []
        total_price = 0
        ticket_price = 20  # Price per ticket

        for show in shows:
            ticket_count = cart[str(show.id)]
            total_price += ticket_count * ticket_price  # Calculate total price
            cart_items.append({
                'show': show,
                'ticket_count': ticket_count,
                'total_show_price': ticket_count * ticket_price,  # Price for this show
            })

        return render(request, 'booking/cart.html', {
            'cart_items': cart_items,
            'total_price': total_price,
        })

class AddToCartView(View):
    def get(self, request, match_id):
        # This will return an error page or redirect if the user tries to access this URL via GET
        return HttpResponse("Method Not Allowed: Please add tickets to the cart via the form.")
    
    def post(self, request, match_id):
        match = get_object_or_404(Show, id=match_id)
        ticket_count = int(request.POST.get('num_tickets', 1))  # Get the number of tickets
        
        # Check if there are enough available seats
        if ticket_count <= match.available_seats:
            # Add the match to the user's cart
            cart_item, created = Cart.objects.get_or_create(user=request.user, show=match)
            if not created:
                cart_item.ticket_count += ticket_count  # Increment ticket count if already in the cart
            cart_item.save()

            # Reduce the available seats of the match
            match.available_seats -= ticket_count
            match.save()

            return redirect('cart')  # Redirect to the cart view
        else:
            return HttpResponse("Not enough available seats.")


class RemoveFromCartView(View):
    def post(self, request, match_id):
        logger.info(f"Removing match_id: {match_id} for user: {request.user.username}")

        try:
            # Try to get the cart item
            cart_item = Cart.objects.get(user=request.user, show_id=match_id)
            logger.info(f"Found cart item: {cart_item}")
            cart_item.delete()  # Delete the cart item
            return redirect('cart')  # Redirect back to the cart page
        except Cart.DoesNotExist:
            # If the cart item doesn't exist, log the error
            logger.warning(f"Cart item with match_id: {match_id} for user: {request.user.username} does not exist.")
            return HttpResponse("The item you tried to remove is not in your cart.")


class OrderConfirmationView(View):
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.ticket_count * 20 for item in cart_items)  # Assuming ticket price is $20

        # Create booking history entries
        for item in cart_items:
            BookingHistory.objects.create(
                user=request.user,
                show=item.show,
                ticket_count=item.ticket_count
            )

        # Clear the cart after order confirmation
        cart_items.delete()

        return render(request, 'booking/order_confirmation.html', {
            'cart_items': cart_items,
            'total_price': total_price,
        })


class BookingHistoryView(View):
    def get(self, request):
        bookings = BookingHistory.objects.filter(user=request.user)
        return render(request, 'booking/booking_history.html', {'bookings': bookings})


def order_confirmation(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.ticket_count * item.show.price for item in cart_items)

    return render(request, 'booking/order_confirmation.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def add_to_cart(request, show_id):
    # Fetch the show based on the provided show_id
    match = get_object_or_404(Show, id=show_id)
    
    # Get ticket count from the form data, default to 1 if not provided
    try:
        ticket_count = int(request.POST.get('ticket_count', 1))  # Default to 1 if no ticket count is provided
    except ValueError:
        return HttpResponse("Invalid ticket count", status=400)

    # Check if there are enough available seats for the requested ticket count
    if not match.is_available(ticket_count):
        return HttpResponse("Not enough available seats.", status=400)

    # Get or create the cart item for the current user and show
    cart_item, created = Cart.objects.get_or_create(user=request.user, show=match)

    if not created:
        # If cart item exists, update the ticket count by adding the new tickets
        cart_item.ticket_count += ticket_count
    else:
        # If cart item is newly created, set the ticket count to the requested value
        cart_item.ticket_count = ticket_count

    # Save the cart item to update the database
    cart_item.save()

    # Update the show’s available seats
    match.update_available_seats(ticket_count)

    return redirect('cart')  # Redirect to the cart page after adding the tickets

def view_cart(request):
    # Fetch the current user's cart items
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, cart_id):
    # Fetch the cart item to be removed
    cart_item = get_object_or_404(Cart, id=cart_id)
    
    # Remove the item from the cart and update available seats
    cart_item.remove_from_cart()

    return redirect('cart')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Show, Cart, BookingHistory
from .forms import ShowForm, CartForm, BookingHistoryForm
import logging

logger = logging.getLogger(__name__)

# Show management view
@login_required
def show_management(request):
    shows = Show.objects.all()
    return render(request, 'booking/show_management.html', {'shows': shows})

# Add or update show
@login_required
def add_or_edit_show(request, show_id=None):
    if show_id:
        show = get_object_or_404(Show, id=show_id)
    else:
        show = None

    if request.method == 'POST':
        form = ShowForm(request.POST, instance=show)
        if form.is_valid():
            form.save()
            return redirect('show_management')
    else:
        form = ShowForm(instance=show)

    return render(request, 'booking/add_or_edit_show.html', {'form': form, 'show': show})

# Cart management view
@login_required
def cart_management(request):
    carts = Cart.objects.all()
    return render(request, 'booking/cart_management.html', {'carts': carts})

# Delete cart item
@login_required
def delete_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.delete()
    return redirect('cart_management')

# Booking history view
@login_required
def booking_history_management(request):
    bookings = BookingHistory.objects.all()
    return render(request, 'booking/booking_history_management.html', {'bookings': bookings})
