from django import forms

from hubur_apis import models

ACTIVE_CHOICES = ((True, 'Yes'), (False, 'No'))

class CreateBannersForm(forms.ModelForm):

    def clean_position(self):
        if models.Banner.objects.filter(position=self.cleaned_data['position'], position__in=[3,4]).exists():
            raise forms.ValidationError("Banner with this Position already exists.")
    
        return self.cleaned_data['position']

    class Meta:
        model = models.Banner
        exclude = ("i_user",)

        labels = {
            "i_subcatagory": ('Sub-Category')
        }

        widgets = {
            "i_subcatagory": forms.Select(attrs={"class": "form-control"}),
            "position": forms.Select(attrs={"class": "form-control"}),
            "platform": forms.Select(attrs={"class": "form-control"}),
            "url": forms.TextInput(attrs={'class':'form-control'}),
            "is_active": forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        }


class EditBannersForm(forms.ModelForm):

    def clean_position(self):
        if models.Banner.objects.filter(position=self.cleaned_data['position'], position__in=[3,4]).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError("Banner with this Position already exists.")
    
        return self.cleaned_data['position']

    class Meta:
        model = models.Banner
        exclude = ("i_user",)

        labels = {
            "i_subcatagory": ('Sub-Category')
        }

        widgets = {
            "i_subcatagory": forms.Select(attrs={"class": "form-control"}),
            "position": forms.Select(attrs={"class": "form-control"}),
            "platform": forms.Select(attrs={"class": "form-control"}),
            "url": forms.TextInput(attrs={'class':'form-control'}),
            "is_active": forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        }