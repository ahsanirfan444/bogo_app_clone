from django import forms

from hubur_apis import models

ACTIVE_CHOICES = ((True, 'Yes'), (False, 'No'))
ACTIVE_CHOICES_AR = ((True, 'نعم'), (False, 'لا'))

class CreateBannersForm(forms.ModelForm):
    def __init__(self, request, current_language, *args, **kwargs):
        self.current_language = current_language
        super().__init__(*args, **kwargs)
        if request.user.lang_code == 1:
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        else:
            self.fields['i_subcatagory'].choices = (("", "---------") if i==0 else (choice.id, choice.name_ar) for i, choice in enumerate(models.SubCategories.objects.filter(is_active=True)))
            self.fields['position'].widget = forms.Select(attrs={"class": "form-control"}, choices=models.Banner.POSITION_CHOICE_AR)
            self.fields['platform'].widget = forms.Select(attrs={"class": "form-control"}, choices=models.Banner.PLATFORM_CHOICE_AR)
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES_AR)

    def clean_position(self):
        if models.Banner.objects.filter(position=self.cleaned_data['position'], position__in=[3,4]).exists():
            raise forms.ValidationError(self.current_language['position_exist'])
    
        return self.cleaned_data['position']

    class Meta:
        model = models.Banner
        exclude = ("i_user",)

        labels = {
            "i_subcatagory": ('Sub Category'),
            "language": ('Banner Language')
        }

        widgets = {
            "i_subcatagory": forms.Select(attrs={"class": "form-control"}),
            "position": forms.Select(attrs={"class": "form-control"}),
            "platform": forms.Select(attrs={"class": "form-control"}),
            "language": forms.Select(attrs={"class": "form-control"}),
            "url": forms.TextInput(attrs={'class':'form-control'}),
            "is_active": forms.Select(attrs={"class": "form-control"})
        }


class EditBannersForm(forms.ModelForm):
    def __init__(self, request, current_language, *args, **kwargs):
        self.current_language = current_language
        super().__init__(*args, **kwargs)
        if request.user.lang_code == 1:
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        else:
            self.fields['i_subcatagory'].choices = (("", "---------") if i==0 else (choice.id, choice.name_ar) for i, choice in enumerate(models.SubCategories.objects.filter(is_active=True)))
            self.fields['position'].widget = forms.Select(attrs={"class": "form-control"}, choices=models.Banner.POSITION_CHOICE_AR)
            self.fields['platform'].widget = forms.Select(attrs={"class": "form-control"}, choices=models.Banner.PLATFORM_CHOICE_AR)
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES_AR)

    def clean_position(self):
        if models.Banner.objects.filter(position=self.cleaned_data['position'], position__in=[3,4]).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError(self.current_language['position_exist'])
    
        return self.cleaned_data['position']

    class Meta:
        model = models.Banner
        exclude = ("i_user",)

        labels = {
            "i_subcatagory": ('Sub Category'),
            "language": ('Banner Language')
        }

        widgets = {
            "i_subcatagory": forms.Select(attrs={"class": "form-control"}),
            "position": forms.Select(attrs={"class": "form-control"}),
            "platform": forms.Select(attrs={"class": "form-control"}),
            "language": forms.Select(attrs={"class": "form-control"}),
            "url": forms.TextInput(attrs={'class':'form-control'}),
            "is_active": forms.Select(attrs={"class": "form-control"})
        }