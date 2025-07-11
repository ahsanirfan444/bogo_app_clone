from django import forms
from hubur_apis import models
from django.contrib import admin

class BusinessAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BusinessAdminForm, self).__init__(*args, **kwargs)
        self.fields['i_business'].choices = (("", "---------") if i==0 else (choice.id, choice.name) for i, choice in enumerate(models.Business.objects.filter(is_active=True, is_claimed=2)))
