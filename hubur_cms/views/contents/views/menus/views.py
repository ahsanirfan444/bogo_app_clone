from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from global_methods import create_content_images, delete_content_images
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required
from django.urls import reverse_lazy
from django.contrib import messages
from hubur_cms.forms.content_form import CreateMenuForm, EditMenuForm, ContentForm
from django.views.generic import DeleteView
from datetime import datetime, timedelta

@method_decorator([vendor_required], name="dispatch")
class VendorMenuList(AuthBaseViews):
    TEMPLATE_NAME = "contents/menus/list_all_menus.html"
    CREATE_URL = reverse_lazy('create_menu')
    CREATE_URL_TITLE = "Upload Menu"

    def get(self, request, *args, **kwargs):
        menus = models.Content.objects.filter(content_type=3, i_user=request.user, i_business=self.get_vendor_business())
        images_list = [models.Images.objects.filter(i_content=data, type=4) for data in menus]

        all_offers_list = [models.Offers.objects.filter(i_content=data) for data in menus]
        active_offers_list = [models.Offers.objects.filter(i_content=data, is_active=True, is_expiry=False) for data in menus]
        renewal_offers_list = [models.Offers.objects.filter(i_content=data, end__date=datetime.now().date() + timedelta(days=2), is_active=True, is_expiry=False) for data in menus]
        expired_offers_list = [models.Offers.objects.filter(i_content=data, is_active=False, is_expiry=True) for data in menus]

        menus_list = zip(menus, images_list, all_offers_list)
        active_menus_list = zip(menus, images_list, active_offers_list)
        renewal_menus_list = zip(menus, images_list, renewal_offers_list)
        expired_menus_list = zip(menus, images_list, expired_offers_list)
        

        return self.render({
            'menus_list': menus_list,
            'active_menus_list': active_menus_list,
            'renewal_menus_list': renewal_menus_list,
            'expired_menus_list': expired_menus_list
        })
    

@method_decorator([vendor_required], name="dispatch")
class VendorCreateMenu(AuthBaseViews):
    TEMPLATE_NAME = "contents/menus/create_menus.html"

    def get(self, request, *args, **kwargs):
        form = CreateMenuForm(category=list(self.get_vendor_business().i_subcategory.values_list('id', flat=True)))

        return self.render({"form": form})
    
    def post(self, request, *args, **kwargs):
        form = CreateMenuForm(request.POST, request.FILES, category=list(self.get_vendor_business().i_subcategory.values_list('id', flat=True)))

        try:
            if form.is_valid():
                product_form = ContentForm(request.POST)
                if product_form.is_valid():
                    product_instance = product_form.save(commit=False)
                    product_instance.i_business = self.get_vendor_business()
                    product_instance.content_type = 3
                    product_instance.i_user = request.user
                    product_instance.save()

                    image_instance = create_content_images(request.FILES.getlist('images'), request.user, 4, self.get_vendor_business(), product_instance)
                    if image_instance:
                        messages.success(request, "Menu Uploaded Successfully")
                        return self.redirect(reverse_lazy("list_vendor_menus"))

                else:
                    messages.error(request, "Please correct the errors below")
                    print(product_form.errors.as_data)
                    return self.render({"form": form})
            
            else:
                messages.error(request, "Please correct the errors below")
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, "Something Went Wrong! Unable to Upload a Menu.")
            return self.render({"form": form})
        

@method_decorator([vendor_required], name="dispatch")
class VendorEditMenu(AuthBaseViews):
    TEMPLATE_NAME = "contents/menus/edit_menus.html"

    def get(self, request, content_id, *args, **kwargs):
        inst = models.Content.objects.get(id=content_id, content_type=3)
        product_images = models.Images.objects.filter(i_content_id=content_id)
        images_list = list(product_images.values_list('image', flat=True))
        
        inst.__dict__.update({'i_sub_category': inst.i_sub_category.id})
        form = EditMenuForm(data=inst.__dict__, category=list(self.get_vendor_business().i_subcategory.values_list('id', flat=True)), content_id=content_id)
        
        try:
            del request.session['image_ids']
        except Exception:
            pass

        return self.render({"form": form, "images": product_images, "images_list": images_list})
    
    def post(self, request, content_id, *args, **kwargs):
        inst = models.Content.objects.get(id=content_id, content_type=3)
        form = EditMenuForm(request.POST, request.FILES, category=list(self.get_vendor_business().i_subcategory.values_list('id', flat=True)), content_id=content_id)
        image_ids = request.session.get('image_ids')

        try:
            if form.is_valid():
                product_form = ContentForm(request.POST, instance=inst)
                if product_form.is_valid():
                    product_instance = product_form.save(commit=False)
                    product_instance.i_business = self.get_vendor_business()
                    product_instance.content_type = 3
                    product_instance.i_user = request.user
                    product_instance.save()

                    delete_content_images(image_ids, request.user, 4, self.get_vendor_business())
                    
                    image_instance = create_content_images(request.FILES.getlist('images'), request.user, 4, self.get_vendor_business(), product_instance)
                    if image_instance:
                        messages.success(request, "Menu Updated Successfully")
                        return self.redirect(reverse_lazy("list_vendor_menus"))

                else:
                    messages.error(request, "Please correct the errors below")
                    return self.render({"form": form})
            
            else:
                messages.error(request, "Please correct the errors below")
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, "Something Went Wrong! Unable to Save a Menu.")
            return self.render({"form": form})
    


@method_decorator([vendor_required], name="dispatch")
class VendorDeleteMenu(DeleteView, AuthBaseViews):
    template_name = "contents/menus/confirm_delete_menus.html"
    model = models.Content

    def get_success_url(self):
        return reverse_lazy("list_vendor_menus")
    
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        kwargs.update({"RETURN_URL": reverse_lazy("list_vendor_menus")})
        return super().get_context_data(**kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"'{name}' deleted successfully")
        return HttpResponseRedirect(success_url)