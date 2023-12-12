from django import forms

class CustomMultipleChoiceField(forms.MultipleChoiceField):
    widget=forms.SelectMultiple(attrs={'class': 'searchable-select', 'multiple': 'multiple', 'placeholder': 'Tags'})

    def validate(self, value):
        pass