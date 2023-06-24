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
class VendorVotesList(AuthBaseViews):
    TEMPLATE_NAME = "votes/list_votes.html"

    def get(self, request, *args, **kwargs):
        interest_list = []
        all_votes = models.Voting.objects.filter(i_business=self.get_vendor_business(), vote=True)
        
        for data in all_votes:
            interest = models.UserInterest.objects.filter(i_user=data.i_user).values_list('i_category__name', flat=True)
            interest_list.append(interest)

        
        vote_list = list(zip(all_votes, interest_list))

        page = request.GET.get('page', 1)
        paginator = Paginator(vote_list, 9)

        try:
            vote_list = paginator.page(page)
        except PageNotAnInteger:
            vote_list = paginator.page(1)
        except EmptyPage:
            vote_list = paginator.page(paginator.num_pages)

        pagination =  vote_list

        return self.render({
            'vote_list': vote_list,
            'pagination': pagination
        })
    

@method_decorator([vendor_required], name="dispatch")
class VendorUnVotesList(AuthBaseViews):
    TEMPLATE_NAME = "votes/list_un_votes.html"

    def get(self, request, *args, **kwargs):
        interest_list = []
        all_votes = models.Voting.objects.filter(i_business=self.get_vendor_business(), vote=False)
        
        for data in all_votes:
            interest = models.UserInterest.objects.filter(i_user=data.i_user).values_list('i_category__name', flat=True)
            interest_list.append(interest)

        
        vote_list = list(zip(all_votes, interest_list))

        page = request.GET.get('page', 1)
        paginator = Paginator(vote_list, 9)

        try:
            vote_list = paginator.page(page)
        except PageNotAnInteger:
            vote_list = paginator.page(1)
        except EmptyPage:
            vote_list = paginator.page(paginator.num_pages)

        pagination =  vote_list

        return self.render({
            'vote_list': vote_list,
            'pagination': pagination
        })