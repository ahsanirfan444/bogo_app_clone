from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
from hubur_cms.forms.subscription_form import CreateSubscriptionFeatureForm, CreateSubscriptionForm, EditSubscriptionFeatureForm, EditSubscriptionForm
import notifications
from django.template.loader import render_to_string
from django.views.generic import DeleteView

@method_decorator([admin_required], name="dispatch")
class AdminSubscriptionFeatureList(AuthBaseViews):
    TEMPLATE_NAME = "subscriptions_feature/list_all_subscriptions_feature.html"
    # CREATE_URL = reverse_lazy('create_subscription')
    # CREATE_URL_TITLE = "Create Subscription"

    def get(self, request, sub_id, *args, **kwargs):
        subscription = models.Subscription.objects.get(id=sub_id)
        subscription_features_list = models.SubscriptionFeature.objects.filter(subscription_id=sub_id)

        return self.render({
            'subscription': subscription,
            'subscription_features_list': subscription_features_list
        })
    

@method_decorator([admin_required], name="dispatch")
class AdminCreateSubscriptionFeatureView(AuthBaseViews):
    TEMPLATE_NAME = "subscriptions_feature/create_subscriptions_feature.html"

    def get(self, request, sub_id, *args, **kwargs):
        form = CreateSubscriptionFeatureForm(request, self.getCurrentLanguage(), sub_id)

        return self.render({"form": form})
    
    def post(self, request, sub_id, *args, **kwargs):
        form = CreateSubscriptionFeatureForm(request, self.getCurrentLanguage(), sub_id, request.POST, request.FILES)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, self.getCurrentLanguage()['add_feature'])
                return self.redirect(reverse_lazy("list_subscriptions_feature", kwargs={"sub_id": sub_id}))
            
            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
            return self.render({"form": form})
    

@method_decorator([admin_required], name="dispatch")
class AdminEditSubscriptionFeatureView(AuthBaseViews):
    TEMPLATE_NAME = "subscriptions_feature/edit_subscriptions_feature.html"

    def get(self, request, sub_id, feature_id, *args, **kwargs):
        inst = models.SubscriptionFeature.objects.get(id=feature_id)
        form = EditSubscriptionFeatureForm(request, self.getCurrentLanguage(), sub_id, feature_id, instance=inst)
        return self.render({"form": form})
    
    def post(self, request, sub_id, feature_id, *args, **kwargs):
        try:
            inst = models.SubscriptionFeature.objects.get(id=feature_id)
            form = EditSubscriptionFeatureForm(request, self.getCurrentLanguage(), sub_id, feature_id, request.POST, request.FILES, instance=inst)
            if form.is_valid():
                form.save()
                messages.success(request, self.getCurrentLanguage()['update_feature'])
                return self.redirect(reverse_lazy("list_subscriptions_feature", kwargs={"sub_id": sub_id}))
            
            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
            return self.render({"form": form})
    

@method_decorator([admin_required], name="dispatch")
class AdminDeleteSubscriptionFeatureView(DeleteView, AuthBaseViews):
    template_name = "subscriptions_feature/confirm_delete_subscriptions_feature.html"
    model = models.SubscriptionFeature

    def get_success_url(self):
        return reverse_lazy("list_subscriptions")
    
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        kwargs.update({"RETURN_URL": reverse_lazy("list_subscriptions")})
        return super().get_context_data(**kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.feature_name if request.user.lang_code == 1 else self.object.feature_name_ar
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"'{name}' {self.getCurrentLanguage()['delete_success']}")
        return HttpResponseRedirect(success_url)