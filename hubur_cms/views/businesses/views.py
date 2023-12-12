from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hubur_cms.forms.profile_form import BusinessCatalogueForm, BusinessDetailsForm
from django.db.models import Q
from django.shortcuts import get_object_or_404
import datetime
from django.views.generic import DeleteView

@method_decorator([admin_required], name="dispatch")
class AdminBusinessesList(AuthBaseViews):
    TEMPLATE_NAME = "businesses/list_all_businesses.html"

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search')
        total_businesses = models.Business.objects.all().count()

        if search_query:
            businesses_list = models.Business.objects.filter(Q(name__icontains=search_query) | Q(i_category__name__icontains=search_query))
        else:
            businesses_list = models.Business.objects.all().order_by('-is_claimed')

        page = request.GET.get('page', 1)
        paginator = Paginator(businesses_list, 100)

        try:
            businesses_list = paginator.page(page)
        except PageNotAnInteger:
            businesses_list = paginator.page(1)
        except EmptyPage:
            businesses_list = paginator.page(paginator.num_pages)

        pagination =  businesses_list

        return self.render({
            'businesses_list': businesses_list,
            'pagination': pagination,
            'search': search_query,
            'total_businesses': total_businesses
        })
    
    def post(self, request, *args, **kwargs):
        business_id = request.POST.get('business_id')
        status = request.POST.get('status')
        status = eval(status)

        models.Business.objects.filter(id=business_id).update(is_active=status)

        if status:
            messages.success(request, self.getCurrentLanguage()['activated_success'])
            return self.redirect(reverse_lazy("list_all_businesses"))
        else:
            messages.success(request, self.getCurrentLanguage()['deactivated_success'])
            return self.redirect(reverse_lazy("list_all_businesses"))



@method_decorator([admin_required], name="dispatch")
class AdminBusinessDetail(AuthBaseViews):
    TEMPLATE_NAME = "businesses/business_overview.html"

    def get(self, request, pk, *args, **kwargs):
        business = get_object_or_404(models.Business, id=pk)
    
        total_checkins = models.Checkedin.objects.filter(i_business=business).count()
        total_reviews = models.Reviews.objects.filter(i_business=business).count()
        total_redemptions = models.Redemption.objects.filter(i_content__i_business=business, is_redeemed=True).count()

        return self.render({
            'business': business,
            'nav': 'business_detail_by_admin',
            'total_reviews': total_reviews,
            'current_language': self.getCurrentLanguage(),
            'total_checkins': total_checkins,
            'total_redemptions':total_redemptions,
        })

@method_decorator([admin_required], name="dispatch")
class EditBusinessDetailsByAdmin(AuthBaseViews):
    TEMPLATE_NAME = "businesses/edit_business_details.html"

    def get(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(models.Business, id=pk)
        category = instance.i_category
        i_subcategory = list(instance.i_subcategory.all().values_list('id', flat=True))
        i_attributes = list(instance.i_attributes.all().values_list('id', flat=True))
        tags = list(models.Tags.objects.filter(business=instance).values_list('id', flat=True))
        instance.__dict__.update({'i_subcategory': i_subcategory, 'i_attributes': i_attributes, 'tags': tags,})
        
        form = BusinessDetailsForm(data=instance.__dict__, instance=instance, category=category)

        return self.render({
            'form': form
        })
    
    def post(self, request, pk, *args, **kwargs):
        inst = get_object_or_404(models.Business, id=pk)
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

            return self.redirect(reverse_lazy('business_detail_by_admin', kwargs={'pk': pk}))

        else:
            messages.error(request, self.getCurrentLanguage()['correct_errors'])
            return self.render({"form": form})
@method_decorator([admin_required], name="dispatch")
class AdminBusinessSchedule(AuthBaseViews):
    TEMPLATE_NAME = "businesses/business_schedule.html"

    def get(self, request, pk, *args, **kwargs):
        business = get_object_or_404(models.Business, id=pk)
    
        total_checkins = models.Checkedin.objects.filter(i_business=business).count()
        total_reviews = models.Reviews.objects.filter(i_business=business).count()
        business_schedule = models.BusinessSchedule.objects.filter(i_business=business).order_by('-i_day')
        total_redemptions = models.Redemption.objects.filter(i_content__i_business=business, is_redeemed=True).count()


        return self.render({
            'business': business,
            'nav': 'business_schedule_by_admin',
            'total_reviews': total_reviews,
            'current_language': self.getCurrentLanguage(),
            'total_checkins': total_checkins,
            'business_schedule':business_schedule,
            'total_redemptions':total_redemptions,
        })
    
    def post(self, request, pk, *args, **kwargs):
        schedule_id = request.POST.get('schedule_id')
        status = request.POST.get('status')
        status = eval(status)

        models.BusinessSchedule.objects.filter(id=schedule_id).update(is_active=status)

        if status:
            messages.success(request, "This business hours have enabled successfully")
            return self.redirect(reverse_lazy("business_schedule_by_admin", kwargs={'pk': pk}))
        else:
            messages.success(request, "This business hours have disabled successfully")
            return self.redirect(reverse_lazy("business_schedule_by_admin", kwargs={'pk': pk}))
        
class EditBusinessScheduleByAdmin(AuthBaseViews):
    TEMPLATE_NAME = "businesses/edit_business_schedule.html"

    def get(self, request, pk, *args, **kwargs):
        business = get_object_or_404(models.Business, id=pk)
        business_schedule = models.BusinessSchedule.objects.filter(i_business=business).order_by('-i_day')

        return self.render({
            'business': business,
            'business_schedule': business_schedule
        })
    
    def post(self, request, pk, *args, **kwargs):
        business = get_object_or_404(models.Business, id=pk)
        business_schedule = models.BusinessSchedule.objects.filter(i_business=business).order_by('-i_day')
        start_times = request.POST.getlist('start_time')
        start_times = [start_time for start_time in start_times if start_time != ""]
        end_times = request.POST.getlist('end_time')
        end_times = [end_time for end_time in end_times if end_time != ""]
        days = request.POST.getlist('day')
        days = [int(dayID) for dayID in days if dayID != ""]
        
        business_schedule = zip(days, start_times, end_times)

        total_checkins = models.Checkedin.objects.filter(i_business=business).count()
        total_reviews = models.Reviews.objects.filter(i_business=business).count()
        total_redemptions = models.Redemption.objects.filter(i_content__i_business=business, is_redeemed=True).count()
        
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

                query = models.BusinessSchedule.objects.filter(i_business__id=business.id, i_day__id=day)

                if query.exists():
                    instance = query.first()
                    instance.start_time = start_time
                    instance.end_time = end_time
                    instance.i_business_id = business.id
                    instance.i_day_id = day
                    instance.save()

                else:
                    models.BusinessSchedule.objects.create(start_time=start_time, end_time=end_time, i_business_id=business.id, i_day_id=day)

            messages.success(request, "Changes Updated Successfully")
            return self.redirect(reverse_lazy('business_schedule_by_admin', kwargs={'pk': pk}))

        else:
            return self.render({
                'business_schedule': business_schedule,
                'error': 'Please select atleast one business schedule',
                'business': business,
                'nav': 'business_schedule_by_admin',
                'total_reviews': total_reviews,
                'current_language': self.getCurrentLanguage(),
                'total_checkins': total_checkins,
                'total_redemptions':total_redemptions,
            })

    

@method_decorator([admin_required], name="dispatch")
class AdminBusinessCatalogueDetails(AuthBaseViews):
    TEMPLATE_NAME = "businesses/business_catalogue.html"

    def get_create_url(self, business_id):
        return reverse_lazy('create_business_catalogue_by_admin', kwargs={'business_id': business_id})
    
    CREATE_URL_TITLE = "Add Catalogue"

    def get(self, request, pk, *args, **kwargs):

        business = get_object_or_404(models.Business, id=pk)
        business_catalogue = models.Images.objects.filter(i_business=business, type=1)

    
        total_checkins = models.Checkedin.objects.filter(i_business=business).count()
        total_reviews = models.Reviews.objects.filter(i_business=business).count()
        total_redemptions = models.Redemption.objects.filter(i_content__i_business=business, is_redeemed=True).count()

        create_url = self.get_create_url(business.id)


        
        return self.render({
            'business_catalogue': business_catalogue,
            'nav': 'business_catalogue_by_admin',
            'business': business,
            'total_reviews': total_reviews,
            'vendor_business': self.get_vendor_business(),
            'current_language': self.getCurrentLanguage(),
            'total_checkins': total_checkins,
            'total_redemptions':total_redemptions,
            'business_catalogue':business_catalogue,
            'CREATE_URL': create_url,
        })
    
    def post(self, request, pk, *args, **kwargs):
        cat_id = request.POST.get('cat_id')
        status = request.POST.get('status')
        status = eval(status)

        models.Images.objects.filter(id=cat_id).update(is_active=status)

        if status:
            messages.success(request, "Catalog Activated Successfully")
            return self.redirect(reverse_lazy("business_catalogue_by_admin", kwargs={'pk': pk}))
        else:
            messages.success(request, "Catalog De-activated Successfully")
            return self.redirect(reverse_lazy("business_catalogue_by_admin", kwargs={'pk': pk}))


@method_decorator([admin_required], name="dispatch")
class AdminBusinessStories(AuthBaseViews):
    TEMPLATE_NAME = "businesses/business_stories.html"
    CREATE_URL = reverse_lazy('create_business_catalogue_by_admin')
    CREATE_URL_TITLE = "Add Catalogue"

    def get(self, request, pk, *args, **kwargs):

        business = get_object_or_404(models.Business, id=pk)
        business_catalogue = models.Images.objects.filter(i_business=business, type=1)

    
        total_checkins = models.Checkedin.objects.filter(i_business=business).count()
        total_reviews = models.Reviews.objects.filter(i_business=business).count()
        total_redemptions = models.Redemption.objects.filter(i_content__i_business=business, is_redeemed=True).count()

        
        return self.render({
            'business_catalogue': business_catalogue,
            'nav': 'business_stories_by_id',
            'business': business,
            'total_reviews': total_reviews,
            'vendor_business': self.get_vendor_business(),
            'current_language': self.getCurrentLanguage(),
            'total_checkins': total_checkins,
            'total_redemptions':total_redemptions,
            'business_catalogue':business_catalogue,
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


@method_decorator([admin_required], name="dispatch")
class AdminBusinessReviews(AuthBaseViews):
    TEMPLATE_NAME = "businesses/business_reviews.html"

    def get(self, request ,pk, *args, **kwargs):
        business = get_object_or_404(models.Business, id=pk)
        reviews_list = models.Reviews.objects.filter(i_business=business)

        total_checkins = models.Checkedin.objects.filter(i_business=business).count()
        total_reviews = reviews_list.count()
        total_redemptions = models.Redemption.objects.filter(i_content__i_business=business, is_redeemed=True).count()

        page = request.GET.get('page', 1)
        paginator = Paginator(reviews_list, 10)

        try:
            reviews_list = paginator.page(page)
        except PageNotAnInteger:
            reviews_list = paginator.page(1)
        except EmptyPage:
            reviews_list = paginator.page(paginator.num_pages)

        pagination =  reviews_list

        return self.render({
            'current_language': self.getCurrentLanguage(),
            'reviews_list': reviews_list,
            'business': business,
            'pagination': pagination,
            'total_reviews': total_reviews,
            'total_checkins': total_checkins,
            'total_redemptions':total_redemptions,
            'nav': 'business_reviews_by_admin',
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


class AdminBusinessActiveStoriesList(AuthBaseViews):
    TEMPLATE_NAME = "businesses/list_active_stories.html"

    def get(self, request, pk, *args, **kwargs):
        business = get_object_or_404(models.Business, id=pk)
        active_stories_list = models.Story.objects.filter(i_business=business, is_active=True)

        total_checkins = models.Checkedin.objects.filter(i_business=business).count()
        total_reviews = models.Reviews.objects.filter(i_business=business).count()
        total_redemptions = models.Redemption.objects.filter(i_content__i_business=business, is_redeemed=True).count()

        
        page = request.GET.get('page', 1)
        paginator = Paginator(active_stories_list, 10)

        try:
            active_stories_list = paginator.page(page)
        except PageNotAnInteger:
            active_stories_list = paginator.page(1)
        except EmptyPage:
            active_stories_list = paginator.page(paginator.num_pages)

        pagination =  active_stories_list

        return self.render({
            'current_language': self.getCurrentLanguage(),
            'business': business,
            'active_stories_list': active_stories_list,
            'pagination': pagination,
            'total_reviews': total_reviews,
            'total_checkins': total_checkins,
            'total_redemptions':total_redemptions,
            'nav': 'business_active_stories_by_admin',
        })
    
class AdminBusinessInActiveStoriesList(AuthBaseViews):
    TEMPLATE_NAME = "businesses/list_inactive_stories.html"

    def get(self, request, pk, *args, **kwargs):
        business = get_object_or_404(models.Business, id=pk)
        inactive_stories_list = models.Story.objects.filter(i_business=business, is_active=False)

        total_checkins = models.Checkedin.objects.filter(i_business=business).count()
        total_reviews = models.Reviews.objects.filter(i_business=business).count()
        total_redemptions = models.Redemption.objects.filter(i_content__i_business=business, is_redeemed=True).count()

        
        page = request.GET.get('page', 1)
        paginator = Paginator(inactive_stories_list, 10)

        try:
            inactive_stories_list = paginator.page(page)
        except PageNotAnInteger:
            inactive_stories_list = paginator.page(1)
        except EmptyPage:
            inactive_stories_list = paginator.page(paginator.num_pages)

        pagination =  inactive_stories_list

        return self.render({
            'current_language': self.getCurrentLanguage(),
            'business': business,
            'inactive_stories_list': inactive_stories_list,
            'pagination': pagination,
            'total_reviews': total_reviews,
            'total_checkins': total_checkins,
            'total_redemptions':total_redemptions,
            'nav': 'business_inactive_stories_by_admin',
        })

@method_decorator([admin_required], name="dispatch")
class DeActivateStoriesByAdminView(AuthBaseViews):

    def get(self, request, pk, business_id, *args, **kwargs):
        instance = models.Story.objects.filter(id=pk)
        instance.update(is_active=False)

        messages.success(request, "Story De-activated successfully!")

        return self.redirect(reverse_lazy('business_inactive_stories_by_admin', kwargs={'pk': business_id}))


@method_decorator([admin_required], name="dispatch")
class DeleteStoriesByAdminView(DeleteView, AuthBaseViews):
    template_name = "businesses/confirm_delete.html"
    model = models.Story

    def get_success_url(self):
        business_id = self.kwargs.get('business_id')
        is_active = self.kwargs.get('is_active')
        url_name = 'business_active_stories_by_admin' if is_active.lower() == 'active' else 'business_inactive_stories_by_admin'
        
        return reverse_lazy(url_name, kwargs={'pk': business_id})

    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        business_id = self.kwargs.get('business_id')
        is_active = self.kwargs.get('is_active')
        url_name = 'business_active_stories_by_admin' if is_active.lower() == 'active' else 'business_inactive_stories_by_admin'
        
        kwargs.update({"RETURN_URL": reverse_lazy(url_name, kwargs={'pk': business_id}), "TYPE":"Story"})
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.i_user.get_name()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"Story of '{name}' deleted successfully")
        return HttpResponseRedirect(success_url)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(models.Story, pk=pk)
        return obj
    
@method_decorator([admin_required], name="dispatch")
class DeleteReviewByAdminView(DeleteView, AuthBaseViews):
    template_name = "businesses/confirm_delete.html"
    model = models.Reviews

    def get_success_url(self):
        business_id = self.kwargs.get('business_id')
        
        return reverse_lazy('business_reviews_by_admin', kwargs={'pk': business_id})

    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        business_id = self.kwargs.get('business_id')
        
        kwargs.update({"RETURN_URL": reverse_lazy('business_reviews_by_admin', kwargs={'pk': business_id}), "TYPE":"Review"})
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            name = self.object.i_user.get_name()
        except:
            name = self.object.display_name

        success_url = self.get_success_url()

        self.object.delete()

        messages.success(request, f"Review of '{name}' deleted successfully")
        return HttpResponseRedirect(success_url)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(models.Reviews, pk=pk)
        return obj

@method_decorator([admin_required], name="dispatch")
class SubscriptionPlansByAdmin(AuthBaseViews):
    TEMPLATE_NAME = "businesses/subscription_plans.html"

    def get(self, request, pk, *args, **kwargs):
        all_features = []
        subscription_plans = models.Subscription.objects.filter(is_active=True)
        for plan in subscription_plans:
            feature = models.SubscriptionFeature.objects.filter(subscription=plan)

            all_features.append(feature)

        all_data = zip(subscription_plans, all_features)

        return self.render({
            'subscription_plans': all_data
        })
    
@method_decorator([admin_required], name="dispatch")
class CreateBusinessCatalogueByAdmin(AuthBaseViews):
    TEMPLATE_NAME = "businesses/create_business_catalogue.html"

    def get(self, request, business_id, *args, **kwargs):
        get_object_or_404(models.Business, id=business_id)
        form = BusinessCatalogueForm()

        return self.render({
            'form': form
        })
    
    def post(self, request, business_id, *args, **kwargs):
        business = get_object_or_404(models.Business, id=business_id)
        total_business_catalogue = models.Images.objects.filter(i_business=business, type=1).count()
        form = BusinessCatalogueForm(request.POST, request.FILES)

        if total_business_catalogue <= 9:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.type = 1
                instance.i_business = business
                instance.i_user = request.user
                instance.save()

                messages.success(request, "Catalogue Added Successfully")

                return self.redirect(reverse_lazy('business_catalogue_by_admin', kwargs={'pk': business_id}))

            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        else:
            messages.error(request, "Catalogue maximum limit is 10")
            return self.render({"form": form})


@method_decorator([admin_required], name="dispatch")
class EditBusinessCatalogueByAdmin(AuthBaseViews):
    TEMPLATE_NAME = "businesses/edit_business_catalogue.html"

    def get(self, request, business_id, cat_id, *args, **kwargs):
        get_object_or_404(models.Business, id=business_id)
        business_catalogue = models.Images.objects.get(id=cat_id)
        form = BusinessCatalogueForm(instance=business_catalogue)

        return self.render({
            'form': form
        })
    
    def post(self, request,business_id, cat_id, *args, **kwargs):
        get_object_or_404(models.Business, id=business_id)
        business_catalogue = models.Images.objects.get(id=cat_id)
        form = BusinessCatalogueForm(request.POST, request.FILES, instance=business_catalogue)
        if form.is_valid():
            form.save()

            messages.success(request, "Changes Updated Successfully")
            return self.redirect(reverse_lazy('business_catalogue_by_admin', kwargs={'pk': business_id}))

        else:
            messages.error(request, self.getCurrentLanguage()['correct_errors'])
            return self.render({"form": form})
        

@method_decorator([admin_required], name="dispatch")
class DeleteCatalogueByAdminView(DeleteView, AuthBaseViews):
    template_name = "profile/confirm_delete_business_catalogue.html"
    model = models.Reviews

    def get_success_url(self):
        business_id = self.kwargs.get('business_id')
        
        return reverse_lazy('business_catalogue_by_admin', kwargs={'pk': business_id})

    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        business_id = self.kwargs.get('business_id')
        
        kwargs.update({"RETURN_URL": reverse_lazy('business_catalogue_by_admin', kwargs={'pk': business_id}), "TYPE":"Catalogue"})
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        name = self.object.i_business.name

        success_url = self.get_success_url()

        self.object.delete()

        messages.success(request, f"Catalogue of '{name}' deleted successfully")
        return HttpResponseRedirect(success_url)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('cat_id')
        obj = get_object_or_404(models.Images, pk=pk)
        return obj
