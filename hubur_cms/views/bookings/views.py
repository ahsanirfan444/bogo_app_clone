from core.base import AuthBaseViews
from global_methods import get_booking_number
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
import notifications
from django.template.loader import render_to_string

@method_decorator([vendor_required], name="dispatch")
class VendorBookingsView(AuthBaseViews):
    TEMPLATE_NAME = "bookings/list_all_bookings.html"

    def get(self, request, *args, **kwargs):
        booking_list = models.Booking.objects.all()

        return self.render({
            'booking_list': booking_list
        })
    

@method_decorator([vendor_required], name="dispatch")
class VendorBookingAcceptView(AuthBaseViews):

    def get(self, request, book_id, *args, **kwargs):
        try:
            instance = models.Booking.objects.get(id=book_id)
            instance.status = 2
            instance.save()

            messages.success(request, "Accepted successfully!")

            return self.redirect(reverse_lazy('list_vendor_bookings'))
        
        except Exception:
            messages.error(request, "Something went wrong!")
            return self.redirect(reverse_lazy('list_vendor_bookings'))
        

@method_decorator([vendor_required], name="dispatch")
class VendorBookingCancelView(AuthBaseViews):

    def post(self, request, book_id, *args, **kwargs):
        try:
            instance = models.Booking.objects.get(id=book_id)
            instance.status = 3
            instance.reason = request.POST.get('reason')
            instance.save()

            messages.success(request, "Cancelled successfully!")

            return self.redirect(reverse_lazy('list_vendor_bookings'))
        
        except Exception:
            messages.error(request, "Something went wrong!")
            return self.redirect(reverse_lazy('list_vendor_bookings'))