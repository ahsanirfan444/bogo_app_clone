from django import forms

from hubur_apis import models

ACTIVE_CHOICES = ((True, 'Yes'), (False, 'No'))

class CreateTrendingDiscountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['i_business'].choices = ((choice.id, choice.name) for choice in models.Business.objects.filter(is_active=True, is_claimed=2))


    def clean_name(self):
        if models.TrendingDiscount.objects.filter(name__iexact=self.cleaned_data['name']).exists():
            raise forms.ValidationError("Trending Discount with this Name already exists.")
        
        return self.cleaned_data['name']

    class Meta:
        model = models.TrendingDiscount
        fields = "__all__"

        labels = {
            "i_business": ('Businesses'),
        }

        widgets = {
            "i_business": forms.SelectMultiple(attrs={'class': 'searchable-select', 'multiple': 'multiple', 'placeholder': 'Select Businesses'}),
            "is_active": forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        }


class EditTrendingDiscountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['i_business'].choices = ((choice.id, choice.name) for choice in models.Business.objects.filter(is_active=True, is_claimed=2))

    def clean_name(self):
        if models.TrendingDiscount.objects.filter(name__iexact=self.cleaned_data['name']).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError("Trending Discount with this Name already exists.")
        
        return self.cleaned_data['name']

    class Meta:
        model = models.TrendingDiscount
        fields = "__all__"

        labels = {
            "i_business": ('Businesses'),
        }

        widgets = {
            "i_business": forms.SelectMultiple(attrs={'class': 'searchable-select', 'multiple': 'multiple', 'placeholder': 'Select Businesses'}),
            "is_active": forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        }