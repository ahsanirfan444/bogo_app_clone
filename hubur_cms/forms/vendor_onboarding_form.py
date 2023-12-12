from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from hubur_apis import models

ACTIVE_CHOICES = ((True, 'Yes'), (False, 'No'))

class VendorProfileForm(UserCreationForm):
    username = forms.CharField(widget=forms.HiddenInput(), required=False)
    role = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    country_code = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        request = self.request.get('request')
        instance = models.ClaimBusiness.objects.get(i_business__place_id=request.GET.get('place_id'))
        
        self.fields['email'].initial = instance.business_email
        self.fields['email'].disabled = True

    def clean_email(self):
        if models.UserProfile.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("This Email has already registered")
        
        return self.cleaned_data['email']
    
    def clean_contact(self):
        if models.UserProfile.objects.filter(contact=self.cleaned_data['contact']).exists():
            raise forms.ValidationError("This Contact Number has already registered")
            
        return self.cleaned_data['contact']

    def clean_dob(self):
        try:
            diff = datetime.now().date() - self.cleaned_data['dob']
            years = int(diff.days / 365)
            if years < 18:
                raise forms.ValidationError("Age must be older than 18 years")
            return self.cleaned_data['dob']
        
        except Exception:
            return self.cleaned_data['dob']
    
    class Meta:
        model = models.UserProfile
        exclude = ('is_active', 'is_staff', 'is_type', 'is_verified', 'is_superuser', 'lat', 'long', 'password', 'groups', 'last_login', 'user_permissions', 'address', 'terms_conditions', 'i_country', 'i_city', 'bg_image', 'lang_code',)
        labels = {
            "dob": ('Date of Birth'),
        }
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(attrs={'class':'form-control'})
        }

        def save(self, commit=True):
            user = super(UserCreationForm, self).save(commit=False)
            user.email = self.cleaned_data["email"]
            if commit:
                user.save()
            return user
        

class VendorBusinessRegistrationForm(forms.ModelForm):
    lat = forms.FloatField(widget=forms.HiddenInput(), required=False)
    long = forms.FloatField(widget=forms.HiddenInput(), required=False)
    country_code = forms.CharField(widget=forms.HiddenInput(), required=False)
    is_claimed = forms.BooleanField(widget=forms.HiddenInput(), required=False)

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
        exclude = ('place_id', 'is_active', 'i_user',)
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
            'i_attributes': forms.CheckboxSelectMultiple(),
            'is_featured': forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
        }