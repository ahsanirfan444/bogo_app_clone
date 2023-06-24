from django import forms

from hubur_apis import models

ACTIVE_CHOICES = ((True, 'Yes'), (False, 'No'))

class CreateBrandForm(forms.ModelForm):

    def clean_name(self):
        if models.Brand.objects.filter(name__iexact=self.cleaned_data['name']).exists():
            raise forms.ValidationError("Brand with this Name already exists.")
        
        return self.cleaned_data['name']

    class Meta:
        model = models.Brand
        fields = "__all__"

        widgets = {
            "founded_year": forms.DateInput(attrs={'type': 'date'}),
            "website": forms.TextInput(attrs={'class':'form-control'}),
            "is_active": forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        }


class EditBrandForm(forms.ModelForm):

    def clean_name(self):
        if models.Brand.objects.filter(name__iexact=self.cleaned_data['name']).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError("Brand with this Name already exists.")
        
        return self.cleaned_data['name']

    class Meta:
        model = models.Brand
        fields = "__all__"

        widgets = {
            "founded_year": forms.DateInput(attrs={'type': 'date'}),
            "website": forms.TextInput(attrs={'class':'form-control'}),
            "is_active": forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        }