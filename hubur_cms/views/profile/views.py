from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from core.base import AuthBaseViews
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from hubur_apis import models
from django.conf import settings
import datetime
from hubur_cms.forms.profile_form import BusinessCatalogueForm, ProfileContactSettingsForm, ProfileDetailsForm, BusinessDetailsForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import DeleteView

class ProfileOverview(AuthBaseViews):
    TEMPLATE_NAME = "profile/overview.html"

    def get(self, request, *args, **kwargs):
        
        return self.render({
            'nav': 'overview'
        })
    

class EditProfileDetails(AuthBaseViews):
    TEMPLATE_NAME = "profile/edit_profile_details.html"

    def get(self, request, *args, **kwargs):
        instance = models.UserProfile.objects.get(id=request.user.id)
        form = ProfileDetailsForm(instance=instance)

        return self.render({
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        inst = models.UserProfile.objects.get(id=request.user.id)
        form = ProfileDetailsForm(request.POST, request.FILES, instance=inst)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.username = form.cleaned_data['email'].split('@')[0]
            instance.country_code = form.cleaned_data['country_code']
            instance.save()
            try:
                form.save_m2m()
            except Exception as e:
                pass

            messages.success(request, "Changes Updated Successfully")
            return self.redirect(reverse_lazy('profile_overview'))

        else:
            messages.error(request, "Please correct the errors below")
            return self.render({"form": form})
        

@method_decorator([vendor_required], name="dispatch")
class BusinessDetails(AuthBaseViews):
    TEMPLATE_NAME = "profile/business_details.html"

    def get(self, request, *args, **kwargs):

        return self.render({
            'nav': 'business_details'
        })
    

@method_decorator([vendor_required], name="dispatch")
class EditBusinessDetails(AuthBaseViews):
    TEMPLATE_NAME = "profile/edit_business_details.html"

    def get(self, request, *args, **kwargs):
        instance = self.get_vendor_business()
        form = BusinessDetailsForm(instance=instance, category=instance.i_category)

        return self.render({
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        inst = self.get_vendor_business()
        form = BusinessDetailsForm(request.POST, request.FILES, instance=inst, category=inst.i_category)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.lat = form.cleaned_data['lat']
            instance.long = form.cleaned_data['long']
            instance.save()

            try:
                form.save_m2m()
            except Exception as e:
                pass

            messages.success(request, "Changes Updated Successfully")

            return self.redirect(reverse_lazy('business_details'))

        else:
            messages.error(request, "Please correct the errors below")
            return self.render({"form": form})
    
    
@method_decorator([vendor_required], name="dispatch")
class BusinessSchedule(AuthBaseViews):
    TEMPLATE_NAME = "profile/business_schedule.html"

    def get(self, request, *args, **kwargs):
        business_schedule = models.BusinessSchedule.objects.filter(i_business=self.get_vendor_business()).order_by('-i_day')

        return self.render({
            'business_schedule': business_schedule,
            'nav': 'business_schedule'
        })
    
    def post(self, request, *args, **kwargs):
        schedule_id = request.POST.get('schedule_id')
        status = request.POST.get('status')
        status = eval(status)

        models.BusinessSchedule.objects.filter(id=schedule_id).update(is_active=status)

        if status:
            messages.success(request, "This business hours have enabled successfully")
            return self.redirect(reverse_lazy("business_schedule"))
        else:
            messages.success(request, "This business hours have disabled successfully")
            return self.redirect(reverse_lazy("business_schedule"))
    

@method_decorator([vendor_required], name="dispatch")
class EditBusinessSchedule(AuthBaseViews):
    TEMPLATE_NAME = "profile/edit_business_schedule.html"

    def get(self, request, *args, **kwargs):
        business_schedule = models.BusinessSchedule.objects.filter(i_business=self.get_vendor_business()).order_by('-i_day')

        return self.render({
            'business_schedule': business_schedule
        })
    
    def post(self, request, *args, **kwargs):
        business_schedule = models.BusinessSchedule.objects.filter(i_business=self.get_vendor_business()).order_by('-i_day')
        start_times = request.POST.getlist('start_time')
        start_times = [start_time for start_time in start_times if start_time != ""]
        end_times = request.POST.getlist('end_time')
        end_times = [end_time for end_time in end_times if end_time != ""]
        days = request.POST.getlist('day')
        days = [int(dayID) for dayID in days if dayID != ""]
        
        business_schedule = zip(days, start_times, end_times)
        
        if days:
            for day, start_time, end_time in business_schedule:
                
                try:
                    start_time = datetime.datetime.strptime(start_time, '%H:%M:%S').time()
                except Exception:
                    start_time = datetime.datetime.strptime(start_time, '%H:%M').time()

                try:
                    end_time = datetime.datetime.strptime(end_time, '%H:%M:%S').time()
                except Exception:
                    end_time = datetime.datetime.strptime(end_time, '%H:%M').time()

                query = models.BusinessSchedule.objects.filter(i_business__id=self.get_vendor_business().id, i_day__id=day)

                if query.exists():
                    instance = query.first()
                    instance.start_time = start_time
                    instance.end_time = end_time
                    instance.i_business_id = self.get_vendor_business().id
                    instance.i_day_id = day
                    instance.save()

                else:
                    models.BusinessSchedule.objects.create(start_time=start_time, end_time=end_time, i_business_id=vendor_business.id, i_day_id=day)

            messages.success(request, "Changes Updated Successfully")
            return self.redirect(reverse_lazy('business_schedule'))

        else:  
            return self.render({
                'business_schedule': business_schedule,
                'error': 'Please select atleast one business schedule'
            })
        
@method_decorator([vendor_required], name="dispatch")
class BusinessCatalogueDetails(AuthBaseViews):
    TEMPLATE_NAME = "profile/business_catalogue.html"
    CREATE_URL = reverse_lazy('create_business_catalogue')
    CREATE_URL_TITLE = "Add Catalogue"

    def get(self, request, *args, **kwargs):
        business_catalogue = models.Images.objects.filter(i_business=self.get_vendor_business(), type=1)
        
        return self.render({
            'business_catalogue': business_catalogue,
            'nav': 'business_catalogue'
        })
    
    def post(self, request, *args, **kwargs):
        cat_id = request.POST.get('cat_id')
        status = request.POST.get('status')
        status = eval(status)

        models.Images.objects.filter(id=cat_id).update(is_active=status)

        if status:
            messages.success(request, "Catalog Activated Successfully")
            return self.redirect(reverse_lazy("business_catalogue"))
        else:
            messages.success(request, "Catalog De-activated Successfully")
            return self.redirect(reverse_lazy("business_catalogue"))


@method_decorator([vendor_required], name="dispatch")
class CreateBusinessCatalogue(AuthBaseViews):
    TEMPLATE_NAME = "profile/create_business_catalogue.html"

    def get(self, request, *args, **kwargs):
        form = BusinessCatalogueForm()

        return self.render({
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        total_business_catalogue = models.Images.objects.filter(i_business=self.get_vendor_business(), type=1).count()
        form = BusinessCatalogueForm(request.POST, request.FILES)

        if total_business_catalogue <= 9:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.type = 1
                instance.i_business = self.get_vendor_business()
                instance.i_user = request.user
                instance.save()

                messages.success(request, "Catalogue Added Successfully")

                return self.redirect(reverse_lazy('business_catalogue'))

            else:
                messages.error(request, "Please correct the errors below")
                return self.render({"form": form})
            
        else:
            messages.error(request, "Catalogue maximum limit is 10")
            return self.render({"form": form})


@method_decorator([vendor_required], name="dispatch")
class EditBusinessCatalogue(AuthBaseViews):
    TEMPLATE_NAME = "profile/edit_business_catalogue.html"

    def get(self, request, cat_id, *args, **kwargs):
        business_catalogue = models.Images.objects.get(id=cat_id)
        form = BusinessCatalogueForm(instance=business_catalogue)

        return self.render({
            'form': form
        })
    
    def post(self, request, cat_id, *args, **kwargs):
        business_catalogue = models.Images.objects.get(id=cat_id)
        form = BusinessCatalogueForm(request.POST, request.FILES, instance=business_catalogue)
        if form.is_valid():
            form.save()

            messages.success(request, "Changes Updated Successfully")

            return self.redirect(reverse_lazy('business_catalogue'))

        else:
            messages.error(request, "Please correct the errors below")
            return self.render({"form": form})
        

@method_decorator([vendor_required], name="dispatch")
class DeleteBusinessCatalogue(DeleteView, AuthBaseViews):
    template_name = "profile/confirm_delete_business_catalogue.html"
    model = models.Images

    def get_success_url(self):
        return reverse_lazy("business_catalogue")
    
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        kwargs.update({"RETURN_URL": reverse_lazy("business_catalogue")})
        return super().get_context_data(**kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Catalogue Image Deleted Successfully")
        return HttpResponseRedirect(success_url)
    

@method_decorator([admin_required], name="dispatch")
class ProfileSettings(AuthBaseViews):
    TEMPLATE_NAME = "profile/profile_settings.html"

    def get(self, request, *args, **kwargs):
        contact_instance = models.ContactUs.objects.all().first()
        
        return self.render({
            'contact_details': contact_instance,
            'nav': 'settings'
        })
    

@method_decorator([admin_required], name="dispatch")
class EditProfileContactSettings(AuthBaseViews):
    TEMPLATE_NAME = "profile/edit_profile_contact_settings.html"

    def get(self, request, *args, **kwargs):
        inst = models.ContactUs.objects.all().first()
        form = ProfileContactSettingsForm(instance=inst)

        return self.render({
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        inst = models.ContactUs.objects.all().first()
        form = ProfileContactSettingsForm(request.POST, instance=inst)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.mobile = form.cleaned_data['country_code']+form.cleaned_data['mobile']
            inst.uan = form.cleaned_data['country_code']+form.cleaned_data['uan']
            inst.whatsapp = form.cleaned_data['country_code']+form.cleaned_data['whatsapp']
            inst.save()

            messages.success(request, "Changes Updated Successfully")

            return self.redirect(reverse_lazy('profile_settings'))

        else:
            messages.error(request, "Please correct the errors below")
            return self.render({"form": form})
        

class ChangePassword(AuthBaseViews):
    TEMPLATE_NAME = "profile/change_password.html"

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user)
        return self.render({
            'form': form,
            'nav': 'change_password'
        })

    def post(self, request, *args, **kwargs):

        changePasswordFields = ['csrfmiddlewaretoken',
                                'old_password', 'new_password1', 'new_password2']
        requestPostKeys = list(request.POST.keys())
        if changePasswordFields == requestPostKeys:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(
                    request, "Password has been changed successfully")
                return self.redirect(reverse_lazy("change_password"))
            return self.render({
                'form': form,
                'nav': 'change_password'
            })

        
        return self.render({
            'form': PasswordChangeForm(user=request.user),
            'nav': 'change_password'
        })