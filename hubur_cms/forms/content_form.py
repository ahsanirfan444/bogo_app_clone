from django import forms

from hubur_apis import models
from hubur_cms.custom_fields import CustomMultipleChoiceField

ACTIVE_CHOICES = ((True, 'Yes'), (False, 'No'))

class CreateProductForm(forms.Form):
    name = forms.CharField()
    name_ar = forms.CharField()
    i_sub_category = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}))
    images = forms.FileField(widget=forms.FileInput(attrs={"accept":"image/*", "multiple":'True'}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
    description_ar = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
    i_brand = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}))
    price = forms.FloatField()
    sku = forms.CharField()
    color = forms.CharField(widget=forms.TextInput(attrs={"type":'color'}))
    quantity = forms.IntegerField()
    is_active = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), choices=ACTIVE_CHOICES)
    tags =  CustomMultipleChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category')
        super().__init__(*args, **kwargs)
        self.fields['i_sub_category'].choices = ((choice.id, choice.name) for choice in models.SubCategories.objects.filter(id__in=self.category, is_active=True))
        self.fields['i_sub_category'].label = 'Category'
        self.fields['i_brand'].choices = ((choice.id, choice.name) for choice in models.Brand.objects.filter(is_active=True))
        self.fields['i_brand'].label = 'Brand'
        

    def clean_name(self):
        if models.Content.objects.filter(name=self.cleaned_data['name'], content_type=1).exists():
            raise forms.ValidationError("Product with this name already exists.")
    
        return self.cleaned_data['name']
    

class EditProductForm(forms.Form):
    name = forms.CharField()
    name_ar = forms.CharField()
    i_sub_category = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}))
    images = forms.FileField(widget=forms.FileInput(attrs={"accept":"image/*", "multiple":'True'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
    description_ar = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
    i_brand = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}))
    price = forms.FloatField()
    sku = forms.CharField()
    color = forms.CharField(widget=forms.TextInput(attrs={"type":'color'}))
    quantity = forms.IntegerField()
    is_active = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), choices=ACTIVE_CHOICES)
    tags =  CustomMultipleChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category')
        self.content_id = kwargs.pop('content_id')
        super().__init__(*args, **kwargs)
        self.fields['i_sub_category'].choices = ((choice.id, choice.name) for choice in models.SubCategories.objects.filter(id__in=self.category, is_active=True))
        self.fields['i_sub_category'].label = 'Category'
        self.fields['i_brand'].choices = ((choice.id, choice.name) for choice in models.Brand.objects.filter(is_active=True))
        self.fields['i_brand'].label = 'Brand'
        self.fields['tags'].choices = ((choice.id, choice.name) for choice in models.Tags.objects.filter(content=self.content_id, is_active=True))

    def clean_name(self):
        if models.Content.objects.filter(name=self.cleaned_data['name'], content_type=1).exclude(pk=self.content_id).exists():
            raise forms.ValidationError("Product with this name already exists.")
    
        return self.cleaned_data['name']
    
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if tags:
            for tag in tags:
                if not tag.isdigit():
                    try:
                        new_tag = models.Tags(name=tag, content_id=self.content_id)
                        new_tag.save()
                    except Exception as e:
                        raise forms.ValidationError(str(e))
                
        return tags


class CreateServiceForm(forms.Form):
    name = forms.CharField()
    name_ar = forms.CharField()
    i_sub_category = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}))
    images = forms.FileField(widget=forms.FileInput(attrs={"accept":"image/*", "multiple":'True'}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
    description_ar = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
    price = forms.FloatField()
    code = forms.CharField()
    is_active = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), choices=ACTIVE_CHOICES)
    tags =  CustomMultipleChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category')
        super().__init__(*args, **kwargs)
        self.fields['i_sub_category'].choices = ((choice.id, choice.name) for choice in models.SubCategories.objects.filter(id__in=self.category, is_active=True))
        self.fields['i_sub_category'].label = 'Category'
        

    def clean_name(self):
        if models.Content.objects.filter(name=self.cleaned_data['name'], content_type=2).exists():
            raise forms.ValidationError("Service with this name already exists.")
    
        return self.cleaned_data['name']
    

class EditServiceForm(forms.Form):
    name = forms.CharField()
    name_ar = forms.CharField()
    i_sub_category = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}))
    images = forms.FileField(widget=forms.FileInput(attrs={"accept":"image/*", "multiple":'True'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
    description_ar = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
    price = forms.FloatField()
    code = forms.CharField()
    is_active = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), choices=ACTIVE_CHOICES)
    tags =  CustomMultipleChoiceField(required=False)


    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category')
        self.content_id = kwargs.pop('content_id')
        super().__init__(*args, **kwargs)
        self.fields['i_sub_category'].choices = ((choice.id, choice.name) for choice in models.SubCategories.objects.filter(id__in=self.category, is_active=True))
        self.fields['i_sub_category'].label = 'Category'
        self.fields['tags'].choices = ((choice.id, choice.name) for choice in models.Tags.objects.filter(content=self.content_id, is_active=True))

    def clean_name(self):
        if models.Content.objects.filter(name=self.cleaned_data['name'], content_type=2).exclude(pk=self.content_id).exists():
            raise forms.ValidationError("Service with this name already exists.")
    
        return self.cleaned_data['name']
    

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if tags:
            for tag in tags:
                if not tag.isdigit():
                    try:
                        new_tag = models.Tags(name=tag, content_id=self.content_id)
                        new_tag.save()
                    except Exception as e:
                        raise forms.ValidationError(str(e))
                
        return tags


class CreateMenuForm(forms.Form):
    name = forms.CharField()
    name_ar = forms.CharField()
    i_sub_category = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}))
    images = forms.FileField(widget=forms.FileInput(attrs={"accept":"image/*", "multiple":'True'}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
    description_ar = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
    is_active = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), choices=ACTIVE_CHOICES)
    tags =  CustomMultipleChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category')
        super().__init__(*args, **kwargs)
        self.fields['i_sub_category'].choices = ((choice.id, choice.name) for choice in models.SubCategories.objects.filter(id__in=self.category, is_active=True))
        self.fields['i_sub_category'].label = 'Category'
        

    def clean_name(self):
        if models.Content.objects.filter(name=self.cleaned_data['name'], content_type=3).exists():
            raise forms.ValidationError("Menu with this name already exists.")
    
        return self.cleaned_data['name']
    

class EditMenuForm(forms.Form):
    name = forms.CharField()
    name_ar = forms.CharField()
    i_sub_category = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}))
    images = forms.FileField(widget=forms.FileInput(attrs={"accept":"image/*", "multiple":'True'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
    description_ar = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
    is_active = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), choices=ACTIVE_CHOICES)
    tags =  CustomMultipleChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category')
        self.content_id = kwargs.pop('content_id')
        super().__init__(*args, **kwargs)
        self.fields['i_sub_category'].choices = ((choice.id, choice.name) for choice in models.SubCategories.objects.filter(id__in=self.category, is_active=True))
        self.fields['i_sub_category'].label = 'Category'
        self.fields['tags'].choices = ((choice.id, choice.name) for choice in models.Tags.objects.filter(content=self.content_id, is_active=True))

    def clean_name(self):
        if models.Content.objects.filter(name=self.cleaned_data['name'], content_type=3).exclude(pk=self.content_id).exists():
            raise forms.ValidationError("Menu with this name already exists.")
    
        return self.cleaned_data['name']
    
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if tags:
            for tag in tags:
                if not tag.isdigit():
                    try:
                        new_tag = models.Tags(name=tag, content_id=self.content_id)
                        new_tag.save()
                    except Exception as e:
                        raise forms.ValidationError(str(e))
                
        return tags


class ContentForm(forms.ModelForm):

    class Meta:
        model = models.Content
        exclude = ("i_user", "content_type", )