from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from global_methods import create_content_images, delete_content_images
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import DeleteView
from datetime import datetime, timedelta, time

from hubur_cms.forms.offers_form import CreateOfferForm, EditOfferForm

@method_decorator([vendor_required], name="dispatch")
class VendorOffersList(AuthBaseViews):
    TEMPLATE_NAME = "offers/list_all_offers.html"
    CREATE_URL = reverse_lazy('create_offer')
    CREATE_URL_TITLE = "Create an Offer"

    def get(self, request, *args, **kwargs):
        offers = models.Offers.objects.filter(i_user=request.user, i_business=self.get_vendor_business())
        active_offers = offers.filter(is_active=True, is_expiry=False)
        renewal_offers = offers.filter(end__date=datetime.now().date() + timedelta(days=2), is_active=True, is_expiry=False)
        expired_offers = offers.filter(is_active=False, is_expiry=True)

        return self.render({
            'all_offers': offers,
            'active_offers': active_offers,
            'renewal_offers': renewal_offers,
            'expired_offers': expired_offers
        })
    

@method_decorator([vendor_required], name="dispatch")
class VendorCreateOffer(AuthBaseViews):
    TEMPLATE_NAME = "offers/create_offers.html"

    def get(self, request, *args, **kwargs):
        form = CreateOfferForm(business=self.get_vendor_business())

        return self.render({"form": form})
    
    def post(self, request, *args, **kwargs):
        try:
            form = CreateOfferForm(request.POST, request.FILES, business=self.get_vendor_business())
            if form.is_valid():
                instance = form.save(commit=False)
                
                if form.data['type'] == '1':
                    current_date = datetime.now().date()
                    next_date = (datetime.now() + timedelta(days=1)).date()
                    start = datetime.combine(current_date, time())
                    end = datetime.combine(next_date, time())
                    instance.start = start
                    instance.end = end

                elif form.data['type'] == '2':
                    day_of_week = datetime.now().weekday()
                    current_date = datetime.now().date()
                    next_date = (datetime.now() + timedelta(days=6 - day_of_week)).date()
                    start = datetime.combine(current_date, time())
                    end = datetime.combine(next_date, time())
                    instance.start = start
                    instance.end = end

                elif form.data['type'] == '3':
                    day = datetime.now().day
                    current_date = datetime.now().date()
                    next_date = (datetime.now() + timedelta(days=30 - day)).date()
                    start = datetime.combine(current_date, time())
                    end = datetime.combine(next_date, time())
                    instance.start = start
                    instance.end = end

                elif form.data['type'] == '4':
                    day = datetime.now().day
                    current_date = datetime.now().date()
                    start = datetime.combine(current_date, time())
                    instance.start = start

                instance.i_user = request.user
                instance.i_business = self.get_vendor_business()
                instance.save()

                try:
                    form.save_m2m()
                except Exception:
                    pass

                messages.success(request, "Offer Created Successfully")
                return self.redirect(reverse_lazy("list_vendor_offers"))
            
            else:
                messages.error(request, "Please correct the errors below")
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, "Something Went Wrong! Unable to Create Offer.")
            return self.render({"form": form})
        

@method_decorator([vendor_required], name="dispatch")
class VendorEditOffer(AuthBaseViews):
    TEMPLATE_NAME = "offers/edit_offers.html"

    def get(self, request, offer_id, *args, **kwargs):
        inst = models.Offers.objects.get(id=offer_id)
        form = EditOfferForm(instance=inst, business=self.get_vendor_business())
        return self.render({"form": form})
    
    def post(self, request, offer_id, *args, **kwargs):
        try:
            inst = models.Offers.objects.get(id=offer_id)
            form = EditOfferForm(request.POST, request.FILES, instance=inst, business=self.get_vendor_business())
            if form.is_valid():
                instance = form.save(commit=False)

                if instance.is_expiry:
                    if form.data['type'] == '1':
                        current_date = datetime.now().date()
                        next_date = (datetime.now() + timedelta(days=1)).date()
                        start = datetime.combine(current_date, time())
                        end = datetime.combine(next_date, time())
                        instance.start = start
                        instance.end = end

                    elif form.data['type'] == '2':
                        day_of_week = datetime.now().weekday()
                        current_date = datetime.now().date()
                        next_date = (datetime.now() + timedelta(days=6 - day_of_week)).date()
                        start = datetime.combine(current_date, time())
                        end = datetime.combine(next_date, time())
                        instance.start = start
                        instance.end = end

                    elif form.data['type'] == '3':
                        day = datetime.now().day
                        current_date = datetime.now().date()
                        next_date = (datetime.now() + timedelta(days=30 - day)).date()
                        start = datetime.combine(current_date, time())
                        end = datetime.combine(next_date, time())
                        instance.start = start
                        instance.end = end

                    elif form.data['type'] == '4':
                        day = datetime.now().day
                        current_date = datetime.now().date()
                        start = datetime.combine(current_date, time())
                        instance.start = start

                    instance.is_expiry = False
                    instance.is_active = True
                    instance.save()

                else:
                    instance.save()

                try:
                    form.save_m2m()
                except Exception:
                    pass

                messages.success(request, "Offer Updated Successfully")
                return self.redirect(reverse_lazy("list_vendor_offers"))
            
            else:
                messages.error(request, "Please correct the errors below")
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, "Something Went Wrong! Unable to Save Offer.")
            return self.render({"form": form})
    


@method_decorator([vendor_required], name="dispatch")
class VendorDeleteOffer(DeleteView, AuthBaseViews):
    template_name = "offers/confirm_delete_offers.html"
    model = models.Offers

    def get_success_url(self):
        return reverse_lazy("list_vendor_offers")
    
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        kwargs.update({"RETURN_URL": reverse_lazy("list_vendor_offers")})
        return super().get_context_data(**kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"'{name}' deleted successfully")
        return HttpResponseRedirect(success_url)