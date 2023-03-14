from django.http import JsonResponse
from core.base import NonAuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.urls import reverse_lazy
from hubur_cms.forms.vendor_onboarding_form import VendorBusinessRegistrationForm, VendorProfileForm
import random, notifications, datetime
from django.utils.decorators import method_decorator
from core.decorators import guest_required

@method_decorator([guest_required], name="dispatch")
class SubmitVendorProfileDetails(NonAuthBaseViews):
    TEMPLATE_NAME = "vendor_onboarding/register-profile.html"

    def get(self, request, *args, **kwargs):
        if request.GET.get('place_id'):
            form = VendorProfileForm()

            return self.render({
                'form': form
            })
        
        else:
            return self.redirect(reverse_lazy('login_url'))
    
    def post(self, request, *args, **kwargs):
        form = VendorProfileForm(request.POST, request.FILES)
                
        if form.is_valid():
            instance = form.save(commit=False)
            instance.username = form.cleaned_data['email'].split('@')[0]
            instance.country_code = form.cleaned_data['country_code']
            instance.role = 2
            instance.save()
            try:
                form.save_m2m()
            except Exception as e:
                pass

            request.session['vendorId'] = instance.id
            request.session['place_id'] = request.GET.get('place_id')
            otp_code = random.randint(1000,9999)
            models.OtpToken.objects.create(code=otp_code, i_user_id=instance.id, medium=1)
            models.OtpToken.objects.create(code=otp_code, i_user_id=instance.id, medium=2)

            subject = 'Vendor Verification'
            html_message = "Your otp verification code is %s " % otp_code
            notifications.sendEmailToSingleUser(html_message, instance.email, subject)
            
            return self.redirect(reverse_lazy('verify_vendor_profile_details'))

        return self.render({'form': form})
    

@method_decorator([guest_required], name="dispatch")
class VerifyVendorProfileDetails(NonAuthBaseViews):
    TEMPLATE_NAME = "vendor_onboarding/otp-verification.html"

    def get(self, request, *args, **kwargs):
        if request.session.get('vendorId') and request.session.get('place_id'):
            return self.render({})
        else:
            return self.redirect(reverse_lazy('submit_vendor_profile_details'))
    
    def post(self, request, *args, **kwargs):
        if request.session.get('vendorId') and request.session.get('place_id'):
            otp_code = request.POST.get('otp_code')
            vendorId = request.session.get('vendorId')
            user_instance = models.UserProfile.objects.get(id=vendorId)
            otp_instance = models.OtpToken.objects.filter(i_user=user_instance, code=otp_code)

            if otp_instance.exists():
                user_instance.is_verified = True
                user_instance.save()
                otp_instance.delete()

                return self.redirect(reverse_lazy('submit_vendor_business_details'))
            
            else:
                return self.render({
                    'error': 'Invalid Code'
                })
            
        else:
            return self.redirect(reverse_lazy('submit_vendor_profile_details'))
        

@method_decorator([guest_required], name="dispatch")
class SubmitVendorBusinessDetails(NonAuthBaseViews):
    TEMPLATE_NAME = "vendor_onboarding/register-business.html"

    def get(self, request, *args, **kwargs):
        if request.session.get('vendorId') and request.session.get('place_id'):
            instance = models.Business.objects.get(place_id=request.session.get('place_id'))
            form = VendorBusinessRegistrationForm(instance=instance, category=instance.i_category)

            return self.render({
                'form': form
            })
        else:
            return self.redirect(reverse_lazy('submit_vendor_profile_details'))
    
    def post(self, request, *args, **kwargs):
        if request.session.get('vendorId') and request.session.get('place_id'):
            instance = models.Business.objects.get(place_id=request.session.get('place_id'))
            form = VendorBusinessRegistrationForm(request.POST, request.FILES, instance=instance, category=instance.i_category)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.i_user_id = request.session['vendorId']
                instance.lat = form.cleaned_data['lat']
                instance.long = form.cleaned_data['long']
                instance.is_claimed = 2
                instance.save()

                vendorId = request.session.get('vendorId')
                user_instance = models.UserProfile.objects.get(id=vendorId)
                user_instance.is_active = True
                user_instance.save()

                try:
                    form.save_m2m()
                except Exception as e:
                    pass

                request.session['businessId'] = instance.id

                return self.redirect(reverse_lazy('submit_vendor_business_schedule'))

            return self.render({'form': form})
        
        else:
            return self.redirect(reverse_lazy('submit_vendor_profile_details'))


class FetchSubCategories(NonAuthBaseViews):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            categoryId = request.POST.get('categoryId')
            subcategories = models.SubCategories.objects.filter(i_category=categoryId).values('id', 'name')
            
            return JsonResponse(list(subcategories), safe=False)
             

@method_decorator([guest_required], name="dispatch")
class SubmitVendorBusinessSchedule(NonAuthBaseViews):
    TEMPLATE_NAME = "vendor_onboarding/register-business-schedule.html"

    def get(self, request, *args, **kwargs):
        if request.session.get('vendorId') and request.session.get('businessId') and request.session.get('place_id'):
            week_days = models.BusinessSchedule.objects.filter(i_business_id=request.session.get('businessId')).order_by('-i_day')

            return self.render({
                'week_days': week_days
            })
        else:
            return self.redirect(reverse_lazy('submit_vendor_profile_details'))
    
    def post(self, request, *args, **kwargs):
        if request.session.get('vendorId') and request.session.get('businessId'):
            week_days = models.BusinessSchedule.objects.filter(i_business_id=request.session.get('businessId')).order_by('-i_day')
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

                    query = models.BusinessSchedule.objects.filter(i_business__id=request.session.get('businessId'), i_day__id=day)

                    if query.exists():
                        instance = query.first()
                        instance.start_time = start_time
                        instance.end_time = end_time
                        instance.i_business_id = request.session.get('businessId')
                        instance.i_day_id = day
                        instance.save()

                    else:
                        models.BusinessSchedule.objects.create(start_time=start_time, end_time=end_time, i_business_id=request.session.get('businessId'), i_day_id=day)

                return self.redirect(reverse_lazy('vendor_onboarding_completed'))

            else:  
                return self.render({
                    'week_days': week_days,
                    'error': 'Please select atleast one business schedule'
                })
        
        else:
            return self.redirect(reverse_lazy('submit_vendor_profile_details'))
    

@method_decorator([guest_required], name="dispatch")
class VendorOnboardingCompleted(NonAuthBaseViews):
    TEMPLATE_NAME = "vendor_onboarding/on-boarding-completed.html"

    def get(self, request, *args, **kwargs):
        if request.session.get('vendorId') and request.session.get('businessId'):
            try:
                del request.session['vendorId']
                del request.session['businessId']
                del request.session['place_id']  
            except Exception:
                pass

            return self.render({})
        else:
            return self.redirect(reverse_lazy('submit_vendor_profile_details'))