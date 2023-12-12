from django import forms

from hubur_apis import models

ACTIVE_CHOICES = ((True, 'Yes'), (False, 'No'))
ACTIVE_CHOICES_AR = ((True, 'نعم'), (False, 'لا'))

class CreatePromotionForm(forms.ModelForm):
    def __init__(self, request, current_language, *args, **kwargs):
        self.current_language = current_language
        super().__init__(*args, **kwargs)
        if request.user.lang_code == 1:
            self.fields['i_business'].choices = ((choice.id, choice.name) for choice in models.Business.objects.filter(is_active=True))
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        else:
            self.fields['i_business'].choices = ((choice.id, choice.name_ar) for choice in models.Business.objects.filter(is_active=True))
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES_AR)

    def clean_title(self):
        if models.Campaign.objects.filter(title__iexact=self.cleaned_data['title']).exists():
            raise forms.ValidationError(self.current_language['promotion_exist'])
        
        return self.cleaned_data['title']
    
    def clean_title_ar(self):
        if models.Campaign.objects.filter(title_ar__iexact=self.cleaned_data['title_ar']).exists():
            raise forms.ValidationError(self.current_language['promotion_exist'])
        
        return self.cleaned_data['title_ar']

    class Meta:
        model = models.Campaign
        fields = "__all__"

        labels = {
            "i_business": ('Business'),
        }

        widgets = {
            "i_business": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.Select(attrs={"class": "form-control"})
        }


class EditPromotionForm(forms.ModelForm):
    def __init__(self, request, current_language, *args, **kwargs):
        self.current_language = current_language
        super().__init__(*args, **kwargs)
        if request.user.lang_code == 1:
            self.fields['i_business'].choices = ((choice.id, choice.name) for choice in models.Business.objects.filter(is_active=True))
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        else:
            self.fields['i_business'].choices = ((choice.id, choice.name_ar) for choice in models.Business.objects.filter(is_active=True))
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES_AR)

    def clean_title(self):
        if models.Campaign.objects.filter(title__iexact=self.cleaned_data['title']).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError(self.current_language['promotion_exist'])
        
        return self.cleaned_data['title']
    
    def clean_title_ar(self):
        if models.Campaign.objects.filter(title_ar__iexact=self.cleaned_data['title_ar']).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError(self.current_language['promotion_exist'])
        
        return self.cleaned_data['title_ar']

    class Meta:
        model = models.Campaign
        fields = "__all__"

        labels = {
            "i_business": ('Business'),
        }

        widgets = {
            "i_business": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.Select(attrs={"class": "form-control"})
        }