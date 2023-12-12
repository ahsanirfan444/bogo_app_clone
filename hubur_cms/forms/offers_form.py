from django import forms

from hubur_apis import models

ACTIVE_CHOICES = ((True, 'Yes'), (False, 'No'))

class CreateOfferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.business = kwargs.pop('business')
        super().__init__(*args, **kwargs)
        offers_content_ids = list(models.Offers.objects.filter(i_business=self.business, is_active=True).values_list('i_content', flat=True))
        self.fields['i_content'].choices = ((choice.id, choice.name) for choice in models.Content.objects.filter(i_business=self.business, is_active=True).exclude(id__in=offers_content_ids))
        
        if self.business.i_category.name == "Products":
            self.fields['i_content'].label = 'Select Products'
        elif self.business.i_category.name == "Restaurant":
            self.fields['i_content'].label = 'Select Menus'
        else:
            self.fields['i_content'].label = 'Select Services'


    def clean_name(self):
        if models.Offers.objects.filter(name__iexact=self.cleaned_data['name']).exists():
            raise forms.ValidationError("Offer with this Name already exists.")
        
        return self.cleaned_data['name']
    
    def clean(self):
        data = self.cleaned_data
        if data['discount_type'] == 1 and data['discount_price'] >= 50:
            raise forms.ValidationError({"discount_price" : "Discount price should be less than 50"})
        
        elif data['discount_type'] == 2:
            for price in data['i_content']:
                if data['discount_price'] >= price.price:
                    raise forms.ValidationError({"discount_price" : "Discount price should be less than original price"})
                

    class Meta:
        model = models.Offers
        exclude = ("start", "end", "is_expiry", "i_user", "i_business",)

        widgets = {
            "type": forms.Select(attrs={"class": "form-control"}),
            "discount_type": forms.Select(attrs={"class": "form-control"}),
            "i_content": forms.SelectMultiple(attrs={'class': 'searchable-select', 'multiple': 'multiple'}),
            "is_featured": forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES),
            "is_active": forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        }


class EditOfferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.business = kwargs.pop('business')
        super().__init__(*args, **kwargs)
        offers_content_ids = list(models.Offers.objects.filter(i_business=self.business, is_active=True).values_list('i_content', flat=True))
        current_offers_content_id = list(self.instance.i_content.values_list('id', flat=True))
        try:
            for index in current_offers_content_id:
                offers_content_ids.remove(index)
        except Exception:
            pass
        
        self.fields['i_content'].choices = ((choice.id, choice.name) for choice in models.Content.objects.filter(i_business=self.business, is_active=True).exclude(id__in=offers_content_ids))
        
        if self.business.i_category.name == "Products":
            self.fields['i_content'].label = 'Select Products'
        elif self.business.i_category.name == "Restaurant":
            self.fields['i_content'].label = 'Select Menus'
        else:
            self.fields['i_content'].label = 'Select Services'

    def clean_name(self):
        if models.Offers.objects.filter(name__iexact=self.cleaned_data['name']).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError("Offer with this Name already exists.")
        
        return self.cleaned_data['name']
    
    def clean(self):
        data = self.cleaned_data
        if data['discount_type'] == 1 and data['discount_price'] >= 50:
            raise forms.ValidationError({"discount_price" : "Discount price should be less than 50"})
        
        elif data['discount_type'] == 2:
            for price in data['i_content']:
                if data['discount_price'] >= price.price:
                    raise forms.ValidationError({"discount_price" : "Discount price should be less than original price"})
        

    class Meta:
        model = models.Offers
        exclude = ("start", "end", "is_expiry", "i_user", "i_business",)

        labels = {
            "i_content": ('Products'),
        }

        widgets = {
            "type": forms.Select(attrs={"class": "form-control"}),
            "discount_type": forms.Select(attrs={"class": "form-control"}),
            "i_content": forms.SelectMultiple(attrs={'class': 'searchable-select', 'multiple': 'multiple', 'placeholder': 'Select Products'}),
            "is_featured": forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES),
            "is_active": forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        }