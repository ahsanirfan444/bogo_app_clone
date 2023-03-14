from django import forms

from hubur_apis import models

ACTIVE_CHOICES = ((True, 'Yes'), (False, 'No'))

class CreateSubCategoryForm(forms.ModelForm):

    class Meta:
        model = models.SubCategories
        fields = "__all__"

        labels = {
            "i_category": ('Category'),
        }

        widgets = {
            "i_category": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        }