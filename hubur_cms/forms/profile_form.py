from datetime import datetime
from django import forms
from hubur_apis import models

class ProfileDetailsForm(forms.ModelForm):
    username = forms.CharField(widget=forms.HiddenInput(), required=False)
    role = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    country_code = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean_dob(self):
        diff = datetime.now().date() - self.cleaned_data['dob']
        years = int(diff.days / 365)
        if years < 18:
            raise forms.ValidationError("Age must be older than 18 years")
        return self.cleaned_data['dob']
    
    class Meta:
        model = models.UserProfile
        exclude = ('is_active', 'is_staff', 'is_type', 'is_verified', 'is_superuser', 'lat', 'long', 'password', 'groups', 'last_login', 'user_permissions', 'address', 'terms_conditions')
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
        
    
    class Meta:
        model = models.Business
        exclude = ('place_id', 'is_active', 'i_user', 'is_claimed',)
        labels = {
            "logo_pic": ('Logo'),
            "i_category": ('Category'),
            "i_subcategory": ('Sub-Category')
        }
        widgets = {
            'i_subcategory': forms.CheckboxSelectMultiple(),
            'i_category': forms.Select(attrs={'class':'form-control'})
        }