from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

@method_decorator([admin_required], name="dispatch")
class AdminBusinessesList(AuthBaseViews):
    TEMPLATE_NAME = "businesses/list_all_businesses.html"

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search')
        total_businesses = models.Business.objects.all().count()

        if search_query:
            businesses_list = models.Business.objects.filter(Q(name__icontains=search_query) | Q(i_category__name__icontains=search_query))
        else:
            businesses_list = models.Business.objects.all()

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
            messages.success(request, "Activated Successfully")
            return self.redirect(reverse_lazy("list_all_businesses"))
        else:
            messages.success(request, "De-activated Successfully")
            return self.redirect(reverse_lazy("list_all_businesses"))