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
class VendorReviewsList(AuthBaseViews):
    TEMPLATE_NAME = "rating/list_review.html"

    def get(self, request, *args, **kwargs):
        reviews_list = models.Reviews.objects.filter(i_business=self.get_vendor_business())


        page = request.GET.get('page', 1)
        paginator = Paginator(reviews_list, 9)

        try:
            reviews_list = paginator.page(page)
        except PageNotAnInteger:
            reviews_list = paginator.page(1)
        except EmptyPage:
            reviews_list = paginator.page(paginator.num_pages)

        pagination =  reviews_list

        return self.render({
            'reviews_list': reviews_list,
            'pagination': pagination
        })
    
