from django.urls import reverse_lazy
from core.base import AuthBaseViews
from django.utils.decorators import method_decorator
from core.decorators import vendor_required
from hubur_apis import models
from django.conf import settings
import datetime
from hubur_cms.forms.profile_form import ProfileDetailsForm, BusinessDetailsForm
from django.contrib import messages

class ProfileOverview(AuthBaseViews):
    TEMPLATE_NAME = "profile/overview.html"

    def get(self, request, *args, **kwargs):
        business_id = models.Business.objects.filter(i_user=request.user).values_list('id', flat=True)
        total_checkins = models.Checkedin.objects.filter(i_business__in=business_id).count()
        
        return self.render({
            'total_checkins': total_checkins
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
        vendor_business = models.Business.objects.get(i_user=request.user)
        total_checkins = models.Checkedin.objects.filter(i_business=vendor_business).count()

        return self.render({
            'vendor_business': vendor_business,
            'total_checkins': total_checkins
        })
    

@method_decorator([vendor_required], name="dispatch")
class EditBusinessDetails(AuthBaseViews):
    TEMPLATE_NAME = "profile/edit_business_details.html"

    def get(self, request, *args, **kwargs):
        instance = models.Business.objects.get(i_user=request.user)
        form = BusinessDetailsForm(instance=instance, category=instance.i_category)

        return self.render({
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        inst = models.Business.objects.get(i_user=request.user)
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
        vendor_business = models.Business.objects.get(i_user=request.user)
        business_schedule = models.BusinessSchedule.objects.filter(i_business=vendor_business).order_by('-i_day')
        total_checkins = models.Checkedin.objects.filter(i_business=vendor_business).count()

        return self.render({
            'vendor_business': vendor_business,
            'business_schedule': business_schedule,
            'total_checkins': total_checkins
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
        vendor_business = models.Business.objects.get(i_user=request.user)
        business_schedule = models.BusinessSchedule.objects.filter(i_business=vendor_business).order_by('-i_day')

        return self.render({
            'vendor_business': vendor_business,
            'business_schedule': business_schedule
        })
    
    def post(self, request, *args, **kwargs):
        vendor_business = models.Business.objects.get(i_user=request.user)
        business_schedule = models.BusinessSchedule.objects.filter(i_business=vendor_business).order_by('-i_day')
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

                query = models.BusinessSchedule.objects.filter(i_business__id=vendor_business.id, i_day__id=day)

                if query.exists():
                    instance = query.first()
                    instance.start_time = start_time
                    instance.end_time = end_time
                    instance.i_business_id = vendor_business.id
                    instance.i_day_id = day
                    instance.save()

                else:
                    models.BusinessSchedule.objects.create(start_time=start_time, end_time=end_time, i_business_id=vendor_business.id, i_day_id=day)

            messages.success(request, "Changes Updated Successfully")
            return self.redirect(reverse_lazy('business_schedule'))

        else:  
            return self.render({
                'vendor_business': vendor_business,
                'business_schedule': business_schedule,
                'error': 'Please select atleast one business schedule'
            })
        
@method_decorator([vendor_required], name="dispatch")
class BusinessCheckInDetails(AuthBaseViews):
    TEMPLATE_NAME = "profile/check_ins.html"

    def get(self, request, *args, **kwargs):
        interest_list = []
        business_id = models.Business.objects.filter(i_user=request.user).values_list('id', flat=True)
        total_checkins = models.Checkedin.objects.filter(i_business__in=business_id).count()
        all_checkins = models.Checkedin.objects.filter(i_business__in=business_id)
        for data in all_checkins:
            interest = models.UserInterest.objects.filter(i_user=data.i_user).values_list('i_category__name', flat=True)
            interest_list.append(interest)

        all_data = zip(all_checkins, interest_list)
        
        return self.render({
            'total_checkins': total_checkins,
            'all_data': all_data
        })