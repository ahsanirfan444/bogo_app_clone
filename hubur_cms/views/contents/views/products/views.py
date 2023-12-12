from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from global_methods import create_content_images, create_tags, delete_content_images
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required
from django.urls import reverse_lazy
from django.contrib import messages
from hubur_cms.forms.content_form import CreateProductForm, EditProductForm, ContentForm
from django.views.generic import DeleteView
from datetime import datetime, timedelta

@method_decorator([vendor_required], name="dispatch")
class VendorProductsList(AuthBaseViews):
    TEMPLATE_NAME = "contents/products/list_all_products.html"
    CREATE_URL = reverse_lazy('create_products')
    CREATE_URL_TITLE = "Create Product"

    def get(self, request, *args, **kwargs):
        products = models.Content.objects.filter(content_type=1, i_user=request.user, i_business=self.get_vendor_business())
        images_list = [models.Images.objects.filter(i_content=data, type=2) for data in products]

        all_offers_list = [models.Offers.objects.filter(i_content=data) for data in products]
        active_offers_list = [models.Offers.objects.filter(i_content=data, is_active=True, is_expiry=False) for data in products]
        renewal_offers_list = [models.Offers.objects.filter(i_content=data, end__date=datetime.now().date() + timedelta(days=2), is_active=True, is_expiry=False) for data in products]
        expired_offers_list = [models.Offers.objects.filter(i_content=data, is_active=False, is_expiry=True) for data in products]

        products_list = zip(products, images_list, all_offers_list)
        active_products_list = zip(products, images_list, active_offers_list)
        renewal_products_list = zip(products, images_list, renewal_offers_list)
        expired_products_list = zip(products, images_list, expired_offers_list)
        

        return self.render({
            'products_list': products_list,
            'active_products_list': active_products_list,
            'renewal_products_list': renewal_products_list,
            'expired_products_list': expired_products_list
        })
    

@method_decorator([vendor_required], name="dispatch")
class VendorCreateProducts(AuthBaseViews):
    TEMPLATE_NAME = "contents/products/create_products.html"

    def get(self, request, *args, **kwargs):
        form = CreateProductForm(category=list(self.get_vendor_business().i_subcategory.values_list('id', flat=True)))

        return self.render({"form": form})
    
    def post(self, request, *args, **kwargs):
        form = CreateProductForm(request.POST, request.FILES, category=list(self.get_vendor_business().i_subcategory.values_list('id', flat=True)))

        try:
            if form.is_valid():
                product_form = ContentForm(request.POST)
                if product_form.is_valid():
                    product_instance = product_form.save(commit=False)
                    product_instance.i_business = self.get_vendor_business()
                    product_instance.content_type = 1
                    product_instance.i_user = request.user
                    product_instance.save()

                    create_tags(form.cleaned_data['tags'], product_instance)
                    image_instance = create_content_images(request.FILES.getlist('images'), request.user, 2, self.get_vendor_business(), product_instance)
                    if image_instance:
                        messages.success(request, "Product Added Successfully")
                        return self.redirect(reverse_lazy("list_vendor_products"))

                else:
                    messages.error(request, self.getCurrentLanguage()['correct_errors'])
                    return self.render({"form": form})
            
            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, "Something Went Wrong! Unable to Create a Product.")
            return self.render({"form": form})
        

@method_decorator([vendor_required], name="dispatch")
class VendorEditProducts(AuthBaseViews):
    TEMPLATE_NAME = "contents/products/edit_products.html"

    def get(self, request, content_id, *args, **kwargs):
        inst = models.Content.objects.get(id=content_id, content_type=1)
        product_images = models.Images.objects.filter(i_content_id=content_id)
        images_list = list(product_images.values_list('image', flat=True))
        tags = list(models.Tags.objects.filter(content=inst).values_list('id', flat=True))
        
        inst.__dict__.update({'i_brand': inst.i_brand.id, 'i_sub_category': inst.i_sub_category.id, 'tags': tags})
        form = EditProductForm(data=inst.__dict__, category=list(self.get_vendor_business().i_subcategory.values_list('id', flat=True)), content_id=content_id)
        
        try:
            del request.session['image_ids']
        except Exception:
            pass

        return self.render({"form": form, "images": product_images, "images_list": images_list})
    
    def post(self, request, content_id, *args, **kwargs):
        inst = models.Content.objects.get(id=content_id, content_type=1)
        form = EditProductForm(request.POST, request.FILES, category=list(self.get_vendor_business().i_subcategory.values_list('id', flat=True)), content_id=content_id)
        image_ids = request.session.get('image_ids')

        try:
            if form.is_valid():
                product_form = ContentForm(request.POST, instance=inst)
                if product_form.is_valid():
                    product_instance = product_form.save(commit=False)
                    product_instance.i_business = self.get_vendor_business()
                    product_instance.content_type = 1
                    product_instance.i_user = request.user
                    product_instance.save()

                    delete_content_images(image_ids, request.user, 2, self.get_vendor_business())
                    
                    image_instance = create_content_images(request.FILES.getlist('images'), request.user, 2, self.get_vendor_business(), product_instance)
                    if image_instance:
                        messages.success(request, "Product Updated Successfully")
                        return self.redirect(reverse_lazy("list_vendor_products"))

                else:
                    messages.error(request, self.getCurrentLanguage()['correct_errors'])
                    return self.render({"form": form})
            
            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, "Something Went Wrong! Unable to Save a Product.")
            return self.render({"form": form})
    


@method_decorator([vendor_required], name="dispatch")
class VendorDeleteProducts(DeleteView, AuthBaseViews):
    template_name = "contents/products/confirm_delete_products.html"
    model = models.Content

    def get_success_url(self):
        return reverse_lazy("list_vendor_products")
    
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        kwargs.update({"RETURN_URL": reverse_lazy("list_vendor_products")})
        return super().get_context_data(**kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"'{name}' deleted successfully")
        return HttpResponseRedirect(success_url)