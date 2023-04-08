from django import forms

from hubur_apis import models

ACTIVE_CHOICES = ((True, 'Yes'), (False, 'No'))

class CreateSubCategoryForm(forms.ModelForm):

    def clean_name(self):
        if models.SubCategories.objects.filter(name__iexact=self.cleaned_data['name']).exists():
            raise forms.ValidationError("Sub categories with this Name already exists.")
        
        return self.cleaned_data['name']

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


class EditSubCategoryForm(forms.ModelForm):

    def clean_name(self):
        if models.SubCategories.objects.filter(name__iexact=self.cleaned_data['name']).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError("Sub categories with this Name already exists.")
        
        return self.cleaned_data['name']

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