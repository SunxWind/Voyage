import datetime
import re

from django.core.exceptions import ValidationError
from django.forms import (
  CharField, DateField, Form, ModelForm, IntegerField, ModelChoiceField, Textarea, TextInput, EmailInput, PasswordInput,
  ModelForm, DateInput, NumberInput, FloatField
)
from django.utils import timezone

from viewer.models import Hotel, Airport, Trip, PurchasedTrip  # Country
from django.contrib.auth.forms import UserCreationForm
import calculation


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email']
        """
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}),
        }
        """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'first_name', 'email', 'last_name', 'password1', 'password2']:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


class TripModelForm(ModelForm):
    class Meta:
        model = Trip
        exclude = ['trip',]
        widgets = {
            'departure_date': DateInput(attrs={'placeholder': 'select date', 'type': 'date'}),
            'return_date': DateInput(attrs={'placeholder': 'select date', 'type': 'date'}),
        }

    # def clean_description(self):
    #     # Each sentence will start with Uppercase
    #     initial = self.cleaned_data['description']
    #     sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
    #     return '. '.join(sentence.capitalize() for sentence in sentences)


    # def clean(self):
    #     result = super().clean()
    #     if result['duration'] <= 1:
    #         self.add_error('duration', '')
    #         raise ValidationError(
    #             "The duration of the stay should be equal to or greater than 1"
    #         )
    #     return result


class TripForm(TripModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['duration'] = FloatField(min_value=1)
        self.fields['adult_price'] = FloatField(min_value=0, step_size=1)
        self.fields['child_price'] = FloatField(min_value=0, step_size=1)
        self.fields['adult_places'] = FloatField(min_value=0)
        self.fields['child_places'] = FloatField(min_value=0)
        # self.fields['departure_date'] = DateField(initial=timezone.now(), required=True)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TripPurchaseModelForm(ModelForm):
    class Meta:
        model = PurchasedTrip
        exclude = ('trip',)
        widgets = {
             'birth_date': DateInput(attrs={'placeholder': 'select date', 'type': 'date'}),
        }


class TripPurchaseForm(TripPurchaseModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount_adult'] = FloatField(min_value=1)
        self.fields['amount_child'] = FloatField(min_value=0)
        self.fields['total_price'] = FloatField(
            widget=calculation.FormulaInput('amount_adult')
        )

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
