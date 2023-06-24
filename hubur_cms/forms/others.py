from django import forms
from hubur_apis import models


class OthersForm(forms.ModelForm):

    class Meta:
        model = models.Other
        exclude = ("updated_at", )


class FAQForm(forms.ModelForm):

    class Meta:
        model = models.FAQ
        exclude = ("created_at", )
        widgets = {
            "question": forms.Textarea(attrs={"rows": "3", }),
            "answer": forms.Textarea(attrs={"rows": "3", })
        }