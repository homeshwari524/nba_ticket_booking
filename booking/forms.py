from django import forms
from .models import Show, Cart, BookingHistory

# Form for managing shows
class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ['title', 'team1', 'team2', 'date_time', 'venue', 'available_seats']

# Form for managing cart items (this can be extended as needed)
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'show', 'ticket_count']

# Form for managing booking history (this is just for visualization, usually would not need a form for this)

class BookingHistoryForm(forms.ModelForm):
    class Meta:
        model = BookingHistory
        exclude = ['booking_date']  # Exclude the 'booking_date' field from the form
