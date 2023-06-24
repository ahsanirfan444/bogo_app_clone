from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from global_methods import create_content_images, delete_content_images
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required
from django.urls import reverse_lazy
from django.contrib import messages
from hubur_cms.forms.content_form import CreateServiceForm, EditServiceForm, ContentForm
from django.views.generic import DeleteView
from datetime import datetime, timedelta

@method_decorator([vendor_required], name="dispatch")
class VendorServicesList(AuthBaseViews):
    TEMPLATE_NAME = "contents/health_care_services/list_all_services.html"
    CREATE_URL = reverse_lazy('create_health_care_services')
    CREATE_URL_TITLE = "Create Services"

    def get(self, request, *args, **kwargs):
        services = models.Content.objects.filter(content_type=4, i_user=request.user, i_business=self.get_vendor_business())
        images_list = [models.Images.objects.filter(i_content=data, type=5) for data in services]

        all_offers_list = [models.Offers.objects.filter(i_content=data) for data in services]
        active_offers_list = [models.Offers.objects.filter(i_content=data, is_active=True, is_expiry=False) for data in services]
        renewal_offers_list = [models.Offers.objects.filter(i_content=data, end__date=datetime.now().date() + timedelta(days=2), is_active=True, is_expiry=False) for data in services]
        expired_offers_list = [models.Offers.objects.filter(i_content=data, is_active=False, is_expiry=True) for data in services]

        services_list = zip(services, images_list, all_offers_list)
        active_services_list = zip(services, images_list, active_offers_list)
        renewal_services_list = zip(services, images_list, renewal_offers_list)
        expired_services_list = zip(services, images_list, expired_offers_list)
        

        return self.render({
            'services_list': services_list,
            'active_services_list': active_services_list,
            'renewal_services_list': renewal_services_list,
            'expired_services_list': expired_services_list
        })
    

@method_decorator([vendor_required], name="dispatch")
class VendorCreateServices(AuthBaseViews):
    TEMPLATE_NAME = "contents/health_care_services/create_services.html"

    def get(self, request, *args, **kwargs):
        form = CreateServiceForm(category=list(self.get_vendor_business().i_subcategory.values_list('id', flat=True)))

        return self.render({"form": form})
    
    def post(self, request, *args, **kwargs):
        form = CreateServiceForm(request.POST, request.FILES, category=list(self.get_vendor_business().i_subcategory.values_list('id', flat=True)))

        try:
            if form.is_valid():
                product_form = ContentForm(request.POST)
                if product_form.is_valid():
                    product_instance = product_form.save(commit=False)
                    product_instance.i_business = self.get_vendor_business()
                    product_instance.content_type = 4
                    product_instance.i_user = request.user
                    product_instance.save()

                    image_instance = create_content_images(request.FILES.getlist('images'), request.user, 5, self.get_vendor_business(), product_instance)
                    if image_instance:
                        messages.success(request, "Service Added Successfully")
                        return self.redirect(reverse_lazy("list_vendor_health_care_services"))

                else:
                    messages.error(request, "Please correct the errors below")
                    print(product_form.errors.as_data)
                    return self.render({"form": form})
            
            else:
                messages.error(request, "Please correct the errors below")
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, "Something Went Wrong! Unable to Create a Service.")
            return self.render({"form": form})
        

@method_decorator([vendor_required], name="dispatch")
class VendorEditServices(AuthBaseViews):
    TEMPLATE_NAME = "contents/health_care_services/edit_services.html"

    def get(self, request, content_id, *args, **kwargs):
        inst = models.Content.objects.get(id=content_id, content_type=4)
        product_images = models.Images.objects.filter(i_content_id=content_id)
        images_list = list(product_images.values_list('image', flat=True))
        
        inst.__dict__.update({'i_sub_category': inst.i_sub_category.id})
        form = EditServiceForm(data=inst.__dict__, category=list(self.get_vendor_business().i_subcategory.values_list('id', flat=True)), content_id=content_id)
        
        try:
            del request.session['image_ids']
        except Exception:
            pass

        return self.render({"form": form, "images": product_images, "images_list": images_list})
    
    def post(self, request, content_id, *args, **kwargs):
        inst = models.Content.objects.get(id=content_id, content_type=4)
        form = EditServiceForm(request.POST, request.FILES, category=list(self.get_vendor_business().i_subcategory.values_list('id', flat=True)), content_id=content_id)
        image_ids = request.session.get('image_ids')

        try:
            if form.is_valid():
                product_form = ContentForm(request.POST, instance=inst)
                if product_form.is_valid():
                    product_instance = product_form.save(commit=False)
                    product_instance.i_business = self.get_vendor_business()
                    product_instance.content_type = 4
                    product_instance.i_user = request.user
                    product_instance.save()

                    delete_content_images(image_ids, request.user, 5, self.get_vendor_business())
                    
                    image_instance = create_content_images(request.FILES.getlist('images'), request.user, 5, self.get_vendor_business(), product_instance)
                    if image_instance:
                        messages.success(request, "Service Updated Successfully")
                        return self.redirect(reverse_lazy("list_vendor_health_care_services"))

                else:
                    messages.error(request, "Please correct the errors below")
                    return self.render({"form": form})
            
            else:
                messages.error(request, "Please correct the errors below")
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, "Something Went Wrong! Unable to Save a Service.")
            return self.render({"form": form})
    


@method_decorator([vendor_required], name="dispatch")
class VendorDeleteServices(DeleteView, AuthBaseViews):
    template_name = "contents/health_care_services/confirm_delete_services.html"
    model = models.Content

    def get_success_url(self):
        return reverse_lazy("list_vendor_health_care_services")
    
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        kwargs.update({"RETURN_URL": reverse_lazy("list_vendor_health_care_services")})
        return super().get_context_data(**kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"'{name}' deleted successfully")
        return HttpResponseRedirect(success_url)