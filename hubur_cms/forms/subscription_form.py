from django import forms

from hubur_apis import models

ACTIVE_CHOICES = ((True, 'Yes'), (False, 'No'))
ACTIVE_CHOICES_AR = ((True, 'نعم'), (False, 'لا'))

class CreateSubscriptionForm(forms.ModelForm):
    def __init__(self, request, current_language, *args, **kwargs):
        self.current_language = current_language
        super().__init__(*args, **kwargs)
        if request.user.lang_code == 1:
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
            self.fields['subscription_type'].widget = forms.Select(attrs={"class": "form-control"}, choices=models.Subscription.SUBSCRIPTION_TYPE_CHOICES)
        else:
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES_AR)
            self.fields['subscription_type'].widget = forms.Select(attrs={"class": "form-control"}, choices=models.Subscription.SUBSCRIPTION_TYPE_CHOICES_AR)

    def clean_name(self):
        if models.Subscription.objects.filter(name__iexact=self.cleaned_data['name']).exists():
            raise forms.ValidationError(self.current_language['subscription_exist'])
        
        return self.cleaned_data['name']
    
    def clean_name_ar(self):
        if models.Subscription.objects.filter(name_ar__iexact=self.cleaned_data['name_ar']).exists():
            raise forms.ValidationError(self.current_language['subscription_exist'])
        
        return self.cleaned_data['name_ar']
    
    def clean_duration_months(self):
        if self.cleaned_data['duration_months'] > 12:
            raise forms.ValidationError(self.current_language['month_exceed_value_error'])
        
        return self.cleaned_data['duration_months']

    class Meta:
        model = models.Subscription
        fields = "__all__"

        widgets = {
            "subscription_type": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.Select(attrs={"class": "form-control"})
        }


class EditSubscriptionForm(forms.ModelForm):
    def __init__(self, request, current_language, *args, **kwargs):
        self.current_language = current_language
        super().__init__(*args, **kwargs)
        if request.user.lang_code == 1:
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
            self.fields['subscription_type'].widget = forms.Select(attrs={"class": "form-control"}, choices=models.Subscription.SUBSCRIPTION_TYPE_CHOICES)
        else:
            self.fields['is_active'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES_AR)
            self.fields['subscription_type'].widget = forms.Select(attrs={"class": "form-control"}, choices=models.Subscription.SUBSCRIPTION_TYPE_CHOICES_AR)

    def clean_name(self):
        if models.Subscription.objects.filter(name__iexact=self.cleaned_data['name']).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError(self.current_language['subscription_exist'])
        
        return self.cleaned_data['name']
    
    def clean_name_ar(self):
        if models.Subscription.objects.filter(name_ar__iexact=self.cleaned_data['name_ar']).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError(self.current_language['subscription_exist'])
        
        return self.cleaned_data['name_ar']

    class Meta:
        model = models.Subscription
        fields = "__all__"

        widgets = {
            "subscription_type": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.Select(attrs={"class": "form-control"})
        }

class CreateSubscriptionFeatureForm(forms.ModelForm):
    def __init__(self, request, current_language, sub_id, *args, **kwargs):
        self.current_language = current_language
        self.sub_id = sub_id
        super().__init__(*args, **kwargs)
        if request.user.lang_code == 1:
            self.fields['is_enabled'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
            self.fields['subscription'].choices = ((choice.id, choice.name) for choice in models.Subscription.objects.filter(id=self.sub_id, is_active=True))
        else:
            self.fields['is_enabled'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES_AR)
            self.fields['subscription'].choices = ((choice.id, choice.name_ar) for choice in models.Subscription.objects.filter(id=self.sub_id, is_active=True))

    class Meta:
        model = models.SubscriptionFeature
        fields = "__all__"

        widgets = {
            "subscription": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.Select(attrs={"class": "form-control"})
        }

class EditSubscriptionFeatureForm(forms.ModelForm):
    def __init__(self, request, current_language, sub_id, feature_id, *args, **kwargs):
        self.current_language = current_language
        self.sub_id = sub_id
        self.feature_id = feature_id
        super().__init__(*args, **kwargs)
        if request.user.lang_code == 1:
            self.fields['is_enabled'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES)
            self.fields['subscription'].choices = ((choice.id, choice.name) for choice in models.Subscription.objects.filter(id=self.sub_id, is_active=True))
        else:
            self.fields['is_enabled'].widget = forms.Select(attrs={"class": "form-control"}, choices=ACTIVE_CHOICES_AR)
            self.fields['subscription'].choices = ((choice.id, choice.name_ar) for choice in models.Subscription.objects.filter(id=self.sub_id, is_active=True))

    class Meta:
        model = models.SubscriptionFeature
        fields = "__all__"

        widgets = {
            "subscription": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.Select(attrs={"class": "form-control"})
        }