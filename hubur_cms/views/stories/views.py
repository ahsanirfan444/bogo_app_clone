from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DeleteView

@method_decorator([vendor_required], name="dispatch")
class VendorActiveStoriesList(AuthBaseViews):
    TEMPLATE_NAME = "stories/list_active_stories.html"

    def get(self, request, *args, **kwargs):
        stories_list = models.Story.objects.filter(i_business=self.get_vendor_business(), is_active=True)

        page = request.GET.get('page', 1)
        paginator = Paginator(stories_list, 9)

        try:
            stories_list = paginator.page(page)
        except PageNotAnInteger:
            stories_list = paginator.page(1)
        except EmptyPage:
            stories_list = paginator.page(paginator.num_pages)

        pagination =  stories_list

        return self.render({
            'stories_list': stories_list,
            'pagination': pagination
        })
    

@method_decorator([vendor_required], name="dispatch")
class VendorInActiveStoriesList(AuthBaseViews):
    TEMPLATE_NAME = "stories/list_inactive_stories.html"

    def get(self, request, *args, **kwargs):
        stories_list = models.Story.objects.filter(i_business=self.get_vendor_business(), is_active=False)

        page = request.GET.get('page', 1)
        paginator = Paginator(stories_list, 9)

        try:
            stories_list = paginator.page(page)
        except PageNotAnInteger:
            stories_list = paginator.page(1)
        except EmptyPage:
            stories_list = paginator.page(paginator.num_pages)

        pagination =  stories_list

        return self.render({
            'stories_list': stories_list,
            'pagination': pagination
        })
  

@method_decorator([vendor_required], name="dispatch")
class VendorsDeActivateStoriesView(AuthBaseViews):

    def get(self, request, story_id, *args, **kwargs):
        instance = models.Story.objects.filter(id=story_id)
        instance.update(is_active=False)

        messages.success(request, "Story De-activated successfully!")

        return self.redirect(reverse_lazy('vendor_inactive_stories'))


@method_decorator([vendor_required], name="dispatch")
class VendorsDeleteStoriesView(DeleteView, AuthBaseViews):
    template_name = "stories/confirm_delete_stories.html"
    model = models.Story

    def get_success_url(self):
        return reverse_lazy("vendor_active_stories")
    
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        kwargs.update({"RETURN_URL": reverse_lazy("vendor_active_stories")})
        return super().get_context_data(**kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.i_user.get_name()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"Story of '{name}' deleted successfully")
        return HttpResponseRedirect(success_url)