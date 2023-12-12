from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from core.decorators import admin_required
from core.base import AuthBaseViews
from hubur_apis import models
from hubur_cms.forms.others import OthersForm, FAQForm
from django.contrib import messages
from django.views.generic import DeleteView

@method_decorator([admin_required], name="dispatch")
class FAQView(AuthBaseViews):
    TEMPLATE_NAME = "others/faq.html"

    def get(self, request, *args, **kwargs):
        faqs = models.FAQ.objects.all()
        form = FAQForm()

        return self.render({"faqs": faqs, "form": form,})
    
    def post(self, request, *args, **kwargs):
        try:
            form = FAQForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, self.getCurrentLanguage()['save_success'])
                return self.redirect(request.path)
            
            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
            return self.render({"form": form})


@method_decorator([admin_required], name="dispatch")
class TermsAndConditionView(AuthBaseViews):
    TEMPLATE_NAME = "others/terms_and_condition.html"

    def get(self, request, *args, **kwargs):
        try:
            terms_condition = models.Other.objects.last().terms_condition if request.user.lang_code == 1 else models.Other.objects.last().terms_condition_ar       
        except Exception:
            terms_condition = ""
        return self.render({"terms_condition": terms_condition})
    

    def post(self, request, *args, **kwargs):
        try:
            inst = models.Other.objects.all()

            if inst.count() != 0:
                if request.user.lang_code == 1:
                    terms_condition = request.POST.get("terms_condition")
                    inst.update(terms_condition=terms_condition)
                    messages.success(request, self.getCurrentLanguage()['save_success'])
                else:
                    terms_condition_ar = request.POST.get("terms_condition_ar")
                    inst.update(terms_condition_ar=terms_condition_ar)
                    messages.success(request, self.getCurrentLanguage()['save_success'])

                return self.redirect(request.path)
            
            form = OthersForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, self.getCurrentLanguage()['save_success'])
                return self.redirect(request.path)
            
            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
            return self.render({"terms_condition": request.POST.get("terms_condition")})
    

@method_decorator([admin_required], name="dispatch")
class AboutUsView(AuthBaseViews):
    TEMPLATE_NAME = "others/about_us.html"

    def get(self, request, *args, **kwargs):

        try:
            about_us = models.Other.objects.last().about_us if request.user.lang_code == 1 else models.Other.objects.last().about_us_ar       
        except Exception:
            about_us = ""
        return self.render({"about_us": about_us})
    
    def post(self, request, *args, **kwargs):
        try:
            inst = models.Other.objects.all()

            if inst.count() != 0:
                if request.user.lang_code == 1:
                    about_us = request.POST.get("about_us")
                    inst.update(about_us=about_us)
                    messages.success(request, self.getCurrentLanguage()['save_success'])
                else:
                    about_us_ar = request.POST.get("about_us_ar")
                    inst.update(about_us_ar=about_us_ar)
                    messages.success(request, self.getCurrentLanguage()['save_success'])

                return self.redirect(request.path)
            
            form = OthersForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, self.getCurrentLanguage()['save_success'])
                return self.redirect(request.path)
            
            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
            return self.render({"about_us": request.POST.get("about_us")})


@method_decorator([admin_required], name="dispatch")
class PrivacyPolicyView(AuthBaseViews):
    TEMPLATE_NAME = "others/privacy_policy.html"

    
    def get(self, request, *args, **kwargs):

        try:
            privacy_policies = models.Other.objects.last().privacy_policy if request.user.lang_code == 1 else models.Other.objects.last().privacy_policy_ar
        except Exception:
            privacy_policies = ""
        return self.render({"privacy_policies": privacy_policies})
    

    def post(self, request, *args, **kwargs):
        try:
            inst = models.Other.objects.all()

            if inst.count() != 0:
                if request.user.lang_code == 1:
                    privacy_policies = request.POST.get("privacy_policies")
                    inst.update(privacy_policy=privacy_policies)
                    messages.success(request, self.getCurrentLanguage()['save_success'])
                else:
                    privacy_policies_ar = request.POST.get("privacy_policies_ar")
                    inst.update(privacy_policy_ar=privacy_policies_ar)
                    messages.success(request, self.getCurrentLanguage()['save_success'])

                return self.redirect(request.path)
            
            form = OthersForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, self.getCurrentLanguage()['save_success'])
                return self.redirect(request.path)
            
            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
            return self.render({"privacy_policies": request.POST.get("privacy_policies")})
        

@method_decorator([admin_required], name="dispatch")
class DisclaimerView(AuthBaseViews):
    TEMPLATE_NAME = "others/disclaimer.html"

    
    def get(self, request, *args, **kwargs):

        try:
            disclaimer = models.Other.objects.last().disclaimer if request.user.lang_code == 1 else models.Other.objects.last().disclaimer_ar
        except Exception:
            disclaimer = ""
        return self.render({"disclaimer": disclaimer})
    

    def post(self, request, *args, **kwargs):
        try:
            inst = models.Other.objects.all()

            if inst.count() != 0:
                if request.user.lang_code == 1:
                    disclaimer = request.POST.get("disclaimer")
                    inst.update(disclaimer=disclaimer)
                    messages.success(request, self.getCurrentLanguage()['save_success'])
                else:
                    disclaimer_ar = request.POST.get("disclaimer_ar")
                    inst.update(disclaimer_ar=disclaimer_ar)
                    messages.success(request, self.getCurrentLanguage()['save_success'])

                return self.redirect(request.path)
            
            form = OthersForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, self.getCurrentLanguage()['save_success'])
                return self.redirect(request.path)
            
            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
            return self.render({"disclaimer": request.POST.get("disclaimer")})
        

@method_decorator([admin_required], name="dispatch")
class EditFAQView(AuthBaseViews):
    TEMPLATE_NAME = "others/edit_faqs.html"

    def get(self, request, faq_id, *args, **kwargs):

        inst = models.FAQ.objects.get(id=faq_id)
        form = FAQForm(instance=inst)
        
        return self.render({"form": form})
    
    def post(self, request, faq_id, *args, **kwargs):
        try:
            inst = models.FAQ.objects.get(id=faq_id)
            form = FAQForm(instance=inst, data=request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "FAQ Edited Successfully")
                return self.redirect(reverse_lazy("others_faq"))
            
            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
            return self.render({"form": form})


@method_decorator([admin_required], name="dispatch")
class DeleteFAQView(DeleteView, AuthBaseViews):
    template_name = "others/confirm_delete_faqs.html"
    model = models.FAQ

    def get_success_url(self):
        return reverse_lazy("others_faq")
    
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        kwargs.update({"RETURN_URL": reverse_lazy("others_faq")})
        return super().get_context_data(**kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.question
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"'{name}' deleted successfully")
        return HttpResponseRedirect(success_url)
