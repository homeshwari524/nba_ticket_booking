from django.contrib import admin
from .models import Show, Cart, BookingHistory


# Inline model for Cart to allow editing related Cart items in the Show Admin page
class CartInline(admin.TabularInline):  # You can also use admin.StackedInline for a different style
    model = Cart
    extra = 1  # Number of empty forms to show
    fields = ('user', 'ticket_count')  # Only showing relevant fields for Cart


# Show model admin customization
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'team1', 'team2', 'date_time', 'venue', 'available_seats')
    search_fields = ('title', 'team1', 'team2', 'venue')
    list_filter = ('date_time', 'venue')  # Filter by date and venue
    fieldsets = (
        (None, {
            'fields': ('title', 'team1', 'team2', 'date_time', 'venue', 'available_seats')
        }),
    )
    inlines = [CartInline]  # Add the inline cart editing functionality within the show admin page


# Cart model admin customization
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'show', 'ticket_count')
    search_fields = ('user__username', 'show__title')
    list_filter = ('show',)  # You can filter Cart by Show for better admin navigation


# BookingHistory model admin customization
class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'show', 'ticket_count', 'booking_date')
    search_fields = ('user__username', 'show__title')
    list_filter = ('booking_date',)  # Filter bookings by date


# Register models with the admin site
admin.site.register(Show, ShowAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(BookingHistory, BookingHistoryAdmin)
