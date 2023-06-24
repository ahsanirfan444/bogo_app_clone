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
class VendorVisitorsList(AuthBaseViews):
    TEMPLATE_NAME = "visitors/list_visitors.html"

    def get(self, request, *args, **kwargs):
        interest_list = []
        all_visitors = models.Visited.objects.filter(i_business=self.get_vendor_business())
        
        for data in all_visitors:
            interest = models.UserInterest.objects.filter(i_user=data.i_user).values_list('i_category__name', flat=True)
            interest_list.append(interest)

        
        visitors_list = list(zip(all_visitors, interest_list))

        page = request.GET.get('page', 1)
        paginator = Paginator(visitors_list, 9)

        try:
            visitors_list = paginator.page(page)
        except PageNotAnInteger:
            visitors_list = paginator.page(1)
        except EmptyPage:
            visitors_list = paginator.page(paginator.num_pages)

        pagination =  visitors_list

        return self.render({
            'visitors_list': visitors_list,
            'pagination': pagination
        })