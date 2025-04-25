from django.db import models
from django.contrib.auth.models import User

class Show(models.Model):
    title = models.CharField(max_length=255)
    team1 = models.CharField(max_length=255)
    team2 = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    venue = models.CharField(max_length=255)
    available_seats = models.IntegerField()

    def __str__(self):
        return f"{self.team1} vs {self.team2} - {self.title}"

    def is_available(self, ticket_count):
        """
        Check if there are enough available seats for the requested ticket count.
        """
        return self.available_seats >= ticket_count

    def update_available_seats(self, ticket_count):
        """
        Update the available seats for a show after booking.
        """
        self.available_seats -= ticket_count
        self.save()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    ticket_count = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'show')  # Prevent multiple entries for the same user-show combination

    def __str__(self):
        return f'{self.show.title} - {self.ticket_count} tickets'

    def total_price(self):
        """
        Helper method to calculate the total price for the tickets in the cart.
        Assuming the ticket price is $20.
        """
        ticket_price = 20
        return self.ticket_count * ticket_price

    def remove_from_cart(self):
        """
        Remove the cart item and update the show’s available seats.
        """
        self.show.update_available_seats(-self.ticket_count)
        self.delete()

class BookingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    ticket_count = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.ticket_count} tickets for {self.show.title} on {self.booking_date}"

    def total_price(self):
        """
        Helper method to calculate the total price for the booking.
        Assuming the ticket price is $20.
        """
        ticket_price = 20
        return self.ticket_count * ticket_price
