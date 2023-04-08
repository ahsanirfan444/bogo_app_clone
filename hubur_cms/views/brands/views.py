from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
from hubur_cms.forms.brands_form import CreateBrandForm, EditBrandForm
import notifications
from django.template.loader import render_to_string
from django.views.generic import DeleteView

@method_decorator([admin_required], name="dispatch")
class AdminBrandsList(AuthBaseViews):
    TEMPLATE_NAME = "brands/list_all_brands.html"
    CREATE_URL = reverse_lazy('create_brands')
    CREATE_URL_TITLE = "Create Brands"

    def get(self, request, *args, **kwargs):
        brands_list = models.Brand.objects.all()

        return self.render({
            'brands_list': brands_list
        })
    

@method_decorator([admin_required], name="dispatch")
class AdminCreateBrandsView(AuthBaseViews):
    TEMPLATE_NAME = "brands/create_brands.html"

    def get(self, request, *args, **kwargs):
        form = CreateBrandForm()

        return self.render({"form": form})
    
    def post(self, request, *args, **kwargs):
        try:
            form = CreateBrandForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()

                messages.success(request, "Brands Added Successfully")
                return self.redirect(reverse_lazy("list_brands"))
            
            else:
                messages.error(request, "Please correct the errors below")
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, "Something Went Wrong! Unable to Save Brands.")
            return self.render({"form": form})
    

@method_decorator([admin_required], name="dispatch")
class AdminEditBrandsView(AuthBaseViews):
    TEMPLATE_NAME = "brands/edit_brands.html"

    def get(self, request, brand_id, *args, **kwargs):
        inst = models.Brand.objects.get(id=brand_id)
        form = EditBrandForm(instance=inst)
        return self.render({"form": form})
    
    def post(self, request, brand_id, *args, **kwargs):
        try:
            inst = models.Brand.objects.get(id=brand_id)
            form = EditBrandForm(request.POST, request.FILES, instance=inst)
            if form.is_valid():
                form.save()
                
                messages.success(request, "Brands Edited Successfully")
                return self.redirect(reverse_lazy("list_brands"))
            
            else:
                messages.error(request, "Please correct the errors below")
                return self.render({"form": form})
        
        except Exception:
            messages.error(request, "Something Went Wrong! Unable to Save Brands.")
            return self.render({"form": form})
    

@method_decorator([admin_required], name="dispatch")
class AdminDeleteBrandsView(DeleteView, AuthBaseViews):
    template_name = "brands/confirm_delete_brands.html"
    model = models.Brand

    def get_success_url(self):
        return reverse_lazy("list_brands")
    
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        kwargs.update({"RETURN_URL": reverse_lazy("list_brands")})
        return super().get_context_data(**kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"'{name}' deleted successfully")
        return HttpResponseRedirect(success_url)