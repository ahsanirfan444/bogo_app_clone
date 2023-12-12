from django import forms

from hubur_apis import models

ACTIVE_CHOICES = ((True, 'Yes'), (False, 'No'))

class EditCategoryForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = ("name", "name_ar", "image",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].disabled = True