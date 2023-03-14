from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
from hubur_cms.forms.subcategory_form import CreateSubCategoryForm
import notifications
from django.template.loader import render_to_string
from django.views.generic import DeleteView

@method_decorator([admin_required], name="dispatch")
class AdminSubCategoriesList(AuthBaseViews):
    TEMPLATE_NAME = "sub_categories/list_all_sub_categories.html"
    CREATE_URL = reverse_lazy('create_sub_category')
    CREATE_URL_TITLE = "Create Sub-Category"

    def get(self, request, *args, **kwargs):
        sub_categories_list = models.SubCategories.objects.all()

        return self.render({
            'sub_categories_list': sub_categories_list
        })
    

@method_decorator([admin_required], name="dispatch")
class AdminCreateSubCategoriesView(AuthBaseViews):
    TEMPLATE_NAME = "sub_categories/create_sub_categories.html"

    def get(self, request, *args, **kwargs):
        form = CreateSubCategoryForm()

        return self.render({"form": form})
    
    def post(self, request, *args, **kwargs):
        form = CreateSubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sub-Category Added Successfully")
            return self.redirect(reverse_lazy("list_sub_categories"))
        messages.error(request, "Something Went Wrong! Unable to Save Sub-Category.")
        return self.render({"form": form})
    

@method_decorator([admin_required], name="dispatch")
class AdminEditSubCategoriesView(AuthBaseViews):
    TEMPLATE_NAME = "sub_categories/edit_sub_categories.html"

    def get(self, request, sub_cat_id, *args, **kwargs):
        inst = models.SubCategories.objects.get(id=sub_cat_id)
        form = CreateSubCategoryForm(instance=inst)
        return self.render({"form": form})
    
    def post(self, request, sub_cat_id, *args, **kwargs):
        inst = models.SubCategories.objects.get(id=sub_cat_id)
        form = CreateSubCategoryForm(instance=inst, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sub-Category Edited Successfully")
            return self.redirect(reverse_lazy("list_sub_categories"))
        messages.error(request, "Something Went Wrong! Unable to Save Sub-Category.")
        return self.render({"form": form})
    

@method_decorator([admin_required], name="dispatch")
class AdminDeleteSubCategoriesView(DeleteView, AuthBaseViews):
    template_name = "sub_categories/confirm_delete_sub_categories.html"
    model = models.SubCategories

    def get_success_url(self):
        return reverse_lazy("list_sub_categories")
    
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_default_context())
        kwargs.update({"RETURN_URL": reverse_lazy("list_sub_categories")})
        return super().get_context_data(**kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"'{name}' deleted successfully")
        return HttpResponseRedirect(success_url)