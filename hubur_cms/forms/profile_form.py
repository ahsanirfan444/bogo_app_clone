from datetime import datetime
from django import forms
from hubur_apis import models

class ProfileDetailsForm(forms.ModelForm):
    username = forms.CharField(widget=forms.HiddenInput(), required=False)
    role = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    country_code = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean_dob(self):
        try:
            diff = datetime.now().date() - self.cleaned_data['dob']
            years = int(diff.days / 365)
            if years < 18:
                raise forms.ValidationError("Age must be older than 18 years")
            return self.cleaned_data['dob']
        
        except Exception:
            return self.cleaned_data['dob']
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        self.fields['contact'].disabled = True
    
    class Meta:
        model = models.UserProfile
        exclude = ('is_active', 'is_staff', 'is_type', 'is_verified', 'is_superuser', 'lat', 'long', 'password', 'groups', 'last_login', 'user_permissions', 'address', 'terms_conditions', 'i_country', 'i_city', 'bg_image',)
        labels = {
            "dob": ('Date of Birth'),
        }
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(attrs={'class':'form-control'})
        }
        

class BusinessDetailsForm(forms.ModelForm):
    lat = forms.FloatField(widget=forms.HiddenInput(), required=False)
    long = forms.FloatField(widget=forms.HiddenInput(), required=False)
    country_code = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category')
        super().__init__(*args, **kwargs)
        self.fields['i_subcategory'].queryset  = models.SubCategories.objects.filter(i_category=self.category.id)
        self.fields['i_category'].disabled = True

        fields_to_delete = None
        if not self.instance.i_category.name == "Restaurant":
            fields_to_delete = ('i_attributes',)

        if fields_to_delete:
            for field in fields_to_delete:
                del self.fields[field]
        
    
    class Meta:
        model = models.Business
        exclude = ('place_id', 'is_active', 'i_user', 'is_claimed',)
        labels = {
            "logo_pic": ('Logo'),
            "i_category": ('Category'),
            "i_subcategory": ('Sub-Category'),
            "i_attributes": ('Attributes')
        }
        widgets = {
            'i_subcategory': forms.CheckboxSelectMultiple(),
            'i_category': forms.Select(attrs={'class':'form-control'}),
            'website': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={"rows":3}),
            'i_attributes': forms.CheckboxSelectMultiple()
        }


class BusinessCatalogueForm(forms.ModelForm):    
    
    class Meta:
        model = models.Images
        fields = ('image', )


class ProfileContactSettingsForm(forms.ModelForm):
    country_code = forms.CharField(widget=forms.HiddenInput(attrs={'value':'+971'}), required=False)
    
    class Meta:
        model = models.ContactUs
        exclude = ('updated_at',)

        labels = {
            "uan": ('UAN'),
        }