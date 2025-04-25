
from django.urls import path
from .views import ShowListView, RegisterView, LoginView, LogoutView, CartView, AddToCartView, RemoveFromCartView, OrderConfirmationView, BookingHistoryView
from . import views
urlpatterns = [
    # User-facing views
    path('', ShowListView.as_view(), name='show_list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cart/', CartView.as_view(), name='cart'),
    path('remove_from_cart/<int:match_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('add_to_cart/<int:match_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('order_confirmation/', OrderConfirmationView.as_view(), name='order_confirmation'),
    path('booking_history/', BookingHistoryView.as_view(), name='booking_history'),
    path('view_cart/', views.view_cart, name='view_cart'),

    # Admin functionality views
    path('admin/shows/', views.show_management, name='show_management'),
    path('admin/shows/add/', views.add_or_edit_show, name='add_or_edit_show'),
    path('admin/shows/<int:show_id>/edit/', views.add_or_edit_show, name='add_or_edit_show'),
    path('admin/carts/', views.cart_management, name='cart_management'),
    path('admin/carts/<int:cart_id>/delete/', views.delete_cart_item, name='delete_cart_item'),
    path('admin/booking-history/', views.booking_history_management, name='booking_history_management'),
]
