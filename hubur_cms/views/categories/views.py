from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
import notifications
from django.template.loader import render_to_string

@method_decorator([admin_required], name="dispatch")
class AdminCategoriesList(AuthBaseViews):
    TEMPLATE_NAME = "categories/list_all_categories.html"

    def get(self, request, *args, **kwargs):
        categories_list = models.Category.objects.all()

        return self.render({
            'categories_list': categories_list
        })