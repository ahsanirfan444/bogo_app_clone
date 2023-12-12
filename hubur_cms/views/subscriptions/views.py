from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
from hubur_cms.forms.subscription_form import CreateSubscriptionForm, EditSubscriptionForm
import notifications
from django.template.loader import render_to_string
from django.views.generic import DeleteView

@method_decorator([admin_required], name="dispatch")
class AdminSubscriptionList(AuthBaseViews):
    TEMPLATE_NAME = "subscriptions/list_all_subscriptions.html"
    CREATE_URL = reverse_lazy('create_subscription')
    CREATE_URL_TITLE = "Create Subscription"

    def get(self, request, *args, **kwargs):
        subscriptions_list = models.Subscription.objects.all()

        return self.render({
            'subscriptions_list': subscriptions_list
        })
    

@method_decorator([admin_required], name="dispatch")
class AdminCreateSubscriptionView(AuthBaseViews):
    TEMPLATE_NAME = "subscriptions/create_subscriptions.html"

    def get(self, request, *args, **kwargs):
        form = CreateSubscriptionForm(request, self.getCurrentLanguage())

        return self.render({"form": form})
    
    def post(self, request, *args, **kwargs):
        form = CreateSubscriptionForm(request, self.getCurrentLanguage(), request.POST, request.FILES)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, self.getCurrentLanguage()['add_subscription'])
                return self.redirect(reverse_lazy("list_subscriptions"))
            
            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
            return self.render({"form": form})
    

@method_decorator([admin_required], name="dispatch")
class AdminEditSubscriptionView(AuthBaseViews):
    TEMPLATE_NAME = "subscriptions/edit_subscriptions.html"

    def get(self, request, sub_id, *args, **kwargs):
        inst = models.Subscription.objects.get(id=sub_id)
        form = EditSubscriptionForm(request, self.getCurrentLanguage(), instance=inst)
        return self.render({"form": form})
    
    def post(self, request, sub_id, *args, **kwargs):
        try:
            inst = models.Subscription.objects.get(id=sub_id)
            form = EditSubscriptionForm(request, self.getCurrentLanguage(), request.POST, request.FILES, instance=inst)
            if form.is_valid():
                form.save()
                messages.success(request, self.getCurrentLanguage()['update_subscription'])
                return self.redirect(reverse_lazy("list_subscriptions"))
            
            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
            return self.render({"form": form})
    

@method_decorator([admin_required], name="dispatch")
class AdminDeleteSubscriptionView(DeleteView, AuthBaseViews):
    template_name = "subscriptions/confirm_delete_subscriptions.html"
    model = models.Subscription

    def get_success_url(self):
        return reverse_lazy("list_subscriptions")
    
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        kwargs.update({"RETURN_URL": reverse_lazy("list_subscriptions")})
        return super().get_context_data(**kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name if request.user.lang_code == 1 else self.object.name_ar
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"'{name}' {self.getCurrentLanguage()['delete_success']}")
        return HttpResponseRedirect(success_url)