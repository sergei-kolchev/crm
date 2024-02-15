from django import forms
from django.forms import inlineformset_factory

from medical_cards.models import MedicalCard


# https://evileg.com/en/post/455/

#ChildrenFormset = inlineformset_factory(models.Parent, models.Child, extra=1)
#AddressFormset = inlineformset_factory(models.Child, models.Address, extra=1)


class CreateMedicalCardForm(forms.ModelForm):
    diagnosis = forms.Select()

    class Meta:
        model = MedicalCard
        fields = ('number', 'diagnosis', 'custom_diagnosis', 'hospitalization')

        widgets = {
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "diagnosis": forms.Select(attrs={"class": "form-select"}),
            "custom_diagnosis": forms.Textarea(attrs={"class": "form-control", "rows": 4})
        }

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        return cleaned_data
