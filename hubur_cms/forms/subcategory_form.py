from django import forms

from hubur_apis import models

ACTIVE_CHOICES = ((True, 'Yes'), (False, 'No'))
ACTIVE_CHOICES_AR = ((True, 'نعم'), (False, 'لا'))

class CreateSubCategoryForm(forms.ModelForm):
    def __init__(self, request, current_language, *args, **kwargs):
        self.current_language = current_language
        super().__init__(*args, **kwargs)
        if request.user.lang_code == 1:
            self.fields['i_category'].choices = ((choice.id, choice.name) for choice in models.Category.objects.filter(is_active=True))
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        else:
            self.fields['i_category'].choices = ((choice.id, choice.name_ar) for choice in models.Category.objects.filter(is_active=True))
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES_AR)

    def clean_name(self):
        if models.SubCategories.objects.filter(name__iexact=self.cleaned_data['name']).exists():
            raise forms.ValidationError(self.current_language['sub_category_exist'])
        
        return self.cleaned_data['name']
    
    def clean_name_ar(self):
        if models.SubCategories.objects.filter(name_ar__iexact=self.cleaned_data['name_ar']).exists():
            raise forms.ValidationError(self.current_language['sub_category_exist'])
        
        return self.cleaned_data['name_ar']

    class Meta:
        model = models.SubCategories
        fields = "__all__"

        labels = {
            "i_category": ('Category'),
        }

        widgets = {
            "i_category": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.Select(attrs={"class": "form-control"})
        }


class EditSubCategoryForm(forms.ModelForm):
    def __init__(self, request, current_language, *args, **kwargs):
        self.current_language = current_language
        super().__init__(*args, **kwargs)
        if request.user.lang_code == 1:
            self.fields['i_category'].choices = ((choice.id, choice.name) for choice in models.Category.objects.filter(is_active=True))
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        else:
            self.fields['i_category'].choices = ((choice.id, choice.name_ar) for choice in models.Category.objects.filter(is_active=True))
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES_AR)

    def clean_name(self):
        if models.SubCategories.objects.filter(name__iexact=self.cleaned_data['name']).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError(self.current_language['sub_category_exist'])
        
        return self.cleaned_data['name']
    
    def clean_name_ar(self):
        if models.SubCategories.objects.filter(name_ar__iexact=self.cleaned_data['name_ar']).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError(self.current_language['sub_category_exist'])
        
        return self.cleaned_data['name_ar']

    class Meta:
        model = models.SubCategories
        fields = "__all__"

        labels = {
            "i_category": ('Category'),
        }

        widgets = {
            "i_category": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.Select(attrs={"class": "form-control"})
        }