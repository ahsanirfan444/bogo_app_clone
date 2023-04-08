from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
from hubur_cms.forms.banners_form import CreateBannersForm, EditBannersForm
import notifications
from django.template.loader import render_to_string
from django.views.generic import DeleteView

@method_decorator([admin_required], name="dispatch")
class AdminBannersList(AuthBaseViews):
    TEMPLATE_NAME = "banners/list_all_banners.html"
    CREATE_URL = reverse_lazy('create_banners')
    CREATE_URL_TITLE = "Create Banner"

    def get(self, request, *args, **kwargs):
        banners_list = models.Banner.objects.all()

        return self.render({
            'banners_list': banners_list
        })
    

@method_decorator([admin_required], name="dispatch")
class AdminCreateBannersView(AuthBaseViews):
    TEMPLATE_NAME = "banners/create_banners.html"

    def get(self, request, *args, **kwargs):
        form = CreateBannersForm()

        return self.render({"form": form})
    
    def post(self, request, *args, **kwargs):
        try:
            form = CreateBannersForm(request.POST, request.FILES)
            
            if form.is_valid():
                instance = form.save(commit=False)
                instance.i_user = request.user
                instance.save()

                messages.success(request, "Banner Added Successfully")
                return self.redirect(reverse_lazy("list_banners"))
            
            else:
                messages.error(request, "Please correct the errors below")
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, "Something Went Wrong! Unable to Save Banner.")
            return self.render({"form": form})
    

@method_decorator([admin_required], name="dispatch")
class AdminEditBannersView(AuthBaseViews):
    TEMPLATE_NAME = "banners/edit_banners.html"

    def get(self, request, ban_id, *args, **kwargs):
        inst = models.Banner.objects.get(id=ban_id)
        form = EditBannersForm(instance=inst)
        return self.render({"form": form})
    
    def post(self, request, ban_id, *args, **kwargs):
        try:
            inst = models.Banner.objects.get(id=ban_id)
            form = EditBannersForm(request.POST, request.FILES, instance=inst)
            if form.is_valid():
                if 'image' in request.POST and request.POST.get('i_subcatagory') is not "":
                    instance = form.save(commit=False)
                    instance.image = None
                    instance.save()

                else:
                    form.save()
                
                messages.success(request, "Banner Edited Successfully")
                return self.redirect(reverse_lazy("list_banners"))
            
            else:
                messages.error(request, "Please correct the errors below")
                return self.render({"form": form})
        
        except Exception:
            messages.error(request, "Something Went Wrong! Unable to Save Banner.")
            return self.render({"form": form})
    

@method_decorator([admin_required], name="dispatch")
class AdminDeleteBannersView(DeleteView, AuthBaseViews):
    template_name = "banners/confirm_delete_banners.html"
    model = models.Banner

    def get_success_url(self):
        return reverse_lazy("list_banners")
    
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        kwargs.update({"RETURN_URL": reverse_lazy("list_banners")})
        return super().get_context_data(**kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.get_position_display()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"'{name}' deleted successfully")
        return HttpResponseRedirect(success_url)