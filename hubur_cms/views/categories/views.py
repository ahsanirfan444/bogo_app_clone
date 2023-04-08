from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
from hubur_cms.forms.category_form import EditCategoryForm
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
    

@method_decorator([admin_required], name="dispatch")
class AdminEditCategoriesView(AuthBaseViews):
    TEMPLATE_NAME = "categories/edit_categories.html"

    def get(self, request, cat_id, *args, **kwargs):
        inst = models.Category.objects.get(id=cat_id)
        form = EditCategoryForm(instance=inst)
        return self.render({"form": form})
    
    def post(self, request, cat_id, *args, **kwargs):
        try:
            inst = models.Category.objects.get(id=cat_id)
            form = EditCategoryForm(request.POST, request.FILES, instance=inst)
            if form.is_valid():
                form.save()
                messages.success(request, "Category Edited Successfully")
                return self.redirect(reverse_lazy("list_categories"))
            
            else:
                messages.error(request, "Please correct the errors below")
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, "Something Went Wrong! Unable to Save Category.")
            return self.render({"form": form})