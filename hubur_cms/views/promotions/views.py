from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
from hubur_cms.forms.promotion_form import CreatePromotionForm, EditPromotionForm
import notifications
from django.template.loader import render_to_string
from django.views.generic import DeleteView

@method_decorator([admin_required], name="dispatch")
class AdminPromotionsList(AuthBaseViews):
    TEMPLATE_NAME = "promotions/list_all_promotions.html"
    CREATE_URL = reverse_lazy('create_promotion')
    CREATE_URL_TITLE = "Create Promotion"

    def get(self, request, *args, **kwargs):
        compaign_list = models.Campaign.objects.all()

        return self.render({
            'compaign_list': compaign_list
        })
    

@method_decorator([admin_required], name="dispatch")
class AdminCreatePromotionsView(AuthBaseViews):
    TEMPLATE_NAME = "promotions/create_promotions.html"

    def get(self, request, *args, **kwargs):
        form = CreatePromotionForm(request, self.getCurrentLanguage())

        return self.render({"form": form})
    
    def post(self, request, *args, **kwargs):
        total = models.Campaign.objects.filter(is_active=True).count()
        form = CreatePromotionForm(request, self.getCurrentLanguage(), request.POST, request.FILES)

        if total < 30:
            try:
                if form.is_valid():
                    form.save()
                    messages.success(request, self.getCurrentLanguage()['add_promotion'])
                    return self.redirect(reverse_lazy("list_promotions"))
                
                else:
                    messages.error(request, self.getCurrentLanguage()['correct_errors'])
                    return self.render({"form": form})
                
            except Exception:
                messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
                return self.render({"form": form})
            
        else:
            messages.error(request, "Couldn't add more than 30 business.Try deleting or in-active any.")
            return self.render({"form": form})
    

@method_decorator([admin_required], name="dispatch")
class AdminEditPromotionsView(AuthBaseViews):
    TEMPLATE_NAME = "promotions/edit_promotions.html"

    def get(self, request, promo_id, *args, **kwargs):
        inst = models.Campaign.objects.get(id=promo_id)
        form = EditPromotionForm(request, self.getCurrentLanguage(), instance=inst)
        return self.render({"form": form})
    
    def post(self, request, promo_id, *args, **kwargs):
        try:
            inst = models.Campaign.objects.get(id=promo_id)
            form = EditPromotionForm(request, self.getCurrentLanguage(), request.POST, request.FILES, instance=inst)
            if form.is_valid():
                form.save()
                messages.success(request, self.getCurrentLanguage()['update_promotion'])
                return self.redirect(reverse_lazy("list_promotions"))
            
            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
            return self.render({"form": form})
    

@method_decorator([admin_required], name="dispatch")
class AdminDeletePromotionsView(DeleteView, AuthBaseViews):
    template_name = "promotions/confirm_delete_promotions.html"
    model = models.Campaign

    def get_success_url(self):
        return reverse_lazy("list_promotions")
    
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        kwargs.update({"RETURN_URL": reverse_lazy("list_promotions")})
        return super().get_context_data(**kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.title if request.user.lang_code == 1 else self.object.title_ar
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"'{name}' {self.getCurrentLanguage()['delete_success']}")
        return HttpResponseRedirect(success_url)