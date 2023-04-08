from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
from hubur_cms.forms.trending_discounts_form import EditTrendingDiscountForm, CreateTrendingDiscountForm
import notifications
from django.template.loader import render_to_string
from django.views.generic import DeleteView

@method_decorator([admin_required], name="dispatch")
class AdminTrendingDiscountsList(AuthBaseViews):
    TEMPLATE_NAME = "trending_discounts/list_all_trending_discounts.html"
    CREATE_URL = reverse_lazy('create_trending_discounts')
    CREATE_URL_TITLE = "Create Trending Discounts"

    def get(self, request, *args, **kwargs):
        trending_discounts_list = models.TrendingDiscount.objects.all()

        return self.render({
            'trending_discounts': trending_discounts_list
        })
    

@method_decorator([admin_required], name="dispatch")
class AdminCreateTrendingDiscountsView(AuthBaseViews):
    TEMPLATE_NAME = "trending_discounts/create_trending_discounts.html"

    def get(self, request, *args, **kwargs):
        form = CreateTrendingDiscountForm()

        return self.render({"form": form})
    
    def post(self, request, *args, **kwargs):
        try:
            form = CreateTrendingDiscountForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Trending Discount Created Successfully")
                return self.redirect(reverse_lazy("list_trending_discounts"))
            
            else:
                messages.error(request, "Please correct the errors below")
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, "Something Went Wrong! Unable to Save Trending Discount.")
            return self.render({"form": form})
    

@method_decorator([admin_required], name="dispatch")
class AdminEditTrendingDiscountsView(AuthBaseViews):
    TEMPLATE_NAME = "trending_discounts/edit_trending_discounts.html"

    def get(self, request, discount_id, *args, **kwargs):
        inst = models.TrendingDiscount.objects.get(id=discount_id)
        form = EditTrendingDiscountForm(instance=inst)
        return self.render({"form": form})
    
    def post(self, request, discount_id, *args, **kwargs):
        try:
            inst = models.TrendingDiscount.objects.get(id=discount_id)
            form = EditTrendingDiscountForm(request.POST, request.FILES, instance=inst)
            if form.is_valid():
                form.save()
                messages.success(request, "Trending Discount Edited Successfully")
                return self.redirect(reverse_lazy("list_trending_discounts"))
            
            else:
                messages.error(request, "Please correct the errors below")
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, "Something Went Wrong! Unable to Save Trending Discount.")
            return self.render({"form": form})
    

@method_decorator([admin_required], name="dispatch")
class AdminDeleteTrendingDiscountsView(DeleteView, AuthBaseViews):
    template_name = "trending_discounts/confirm_delete_trending_discounts.html"
    model = models.TrendingDiscount

    def get_success_url(self):
        return reverse_lazy("list_trending_discounts")
    
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        kwargs.update({"RETURN_URL": reverse_lazy("list_trending_discounts")})
        return super().get_context_data(**kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"'{name}' deleted successfully")
        return HttpResponseRedirect(success_url)