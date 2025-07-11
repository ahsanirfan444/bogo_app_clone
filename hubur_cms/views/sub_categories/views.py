from django.http import HttpResponseRedirect
from core.base import AuthBaseViews
from hubur_apis import models
from django.conf import settings
from django.utils.decorators import method_decorator
from core.decorators import vendor_required, admin_required
from django.urls import reverse_lazy
from django.contrib import messages
from hubur_cms.forms.subcategory_form import CreateSubCategoryForm, EditSubCategoryForm
import notifications
from django.template.loader import render_to_string
from django.views.generic import DeleteView

@method_decorator([admin_required], name="dispatch")
class AdminSubCategoriesList(AuthBaseViews):
    TEMPLATE_NAME = "sub_categories/list_all_sub_categories.html"
    CREATE_URL = reverse_lazy('create_sub_category')
    CREATE_URL_TITLE = "Create Sub Category"

    def get(self, request, *args, **kwargs):
        sub_categories_list = models.SubCategories.objects.all()

        return self.render({
            'sub_categories_list': sub_categories_list
        })
    

@method_decorator([admin_required], name="dispatch")
class AdminCreateSubCategoriesView(AuthBaseViews):
    TEMPLATE_NAME = "sub_categories/create_sub_categories.html"

    def get(self, request, *args, **kwargs):
        form = CreateSubCategoryForm(request, self.getCurrentLanguage())

        return self.render({"form": form})
    
    def post(self, request, *args, **kwargs):
        form = CreateSubCategoryForm(request, self.getCurrentLanguage(), request.POST, request.FILES)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, self.getCurrentLanguage()['add_subcategory'])
                return self.redirect(reverse_lazy("list_sub_categories"))
            
            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
            return self.render({"form": form})
    

@method_decorator([admin_required], name="dispatch")
class AdminEditSubCategoriesView(AuthBaseViews):
    TEMPLATE_NAME = "sub_categories/edit_sub_categories.html"

    def get(self, request, sub_cat_id, *args, **kwargs):
        inst = models.SubCategories.objects.get(id=sub_cat_id)
        form = EditSubCategoryForm(request, self.getCurrentLanguage(), instance=inst)
        return self.render({"form": form})
    
    def post(self, request, sub_cat_id, *args, **kwargs):
        try:
            inst = models.SubCategories.objects.get(id=sub_cat_id)
            form = EditSubCategoryForm(request, self.getCurrentLanguage(), request.POST, request.FILES, instance=inst)
            if form.is_valid():
                form.save()
                messages.success(request, self.getCurrentLanguage()['update_subcategory'])
                return self.redirect(reverse_lazy("list_sub_categories"))
            
            else:
                messages.error(request, self.getCurrentLanguage()['correct_errors'])
                return self.render({"form": form})
            
        except Exception:
            messages.error(request, self.getCurrentLanguage()['something_went_wrong'])
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
        name = self.object.name if request.user.lang_code == 1 else self.object.name_ar
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"'{name}' {self.getCurrentLanguage()['delete_success']}")
        return HttpResponseRedirect(success_url)