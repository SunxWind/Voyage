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

    def clean_code(self):
        initial = self.cleaned_data['code']
        print(f"Initial = '{initial}'")
        print(f"Initial length = '{len(initial)}'")
        if initial and len(initial) < 7:
            raise ValidationError("The code should consist of 7 symbols(4 letters and 3 digits).")

        wrong = False
        if initial:
            for i in range(10):
                if str(i) in initial[:4]:
                    wrong = True
            if wrong:
                raise ValidationError("The first four symbols of the code should contain letters only.")
            try:
                int(initial[4:])
            except:
                raise ValidationError("The last three symbols of the code should contain numbers only.")

        print(f"Return length = {len(initial.upper())}")

        return initial.upper()

    def clean_departure_date(self):
        initial = self.cleaned_data['departure_date']
        print(f"Initial = '{initial}'")
        if initial and initial < datetime.date.today():
            raise ValidationError("It is not possible to set the departure date in the past.")
        return initial

    def clean_return_date(self):
        cleaned_data = super().clean()
        initial = self.cleaned_data['return_date']

        print(f"Initial = '{initial}'")
        if initial and initial < datetime.date.today():
            raise ValidationError("It is not possible to set the return date in the past.")

        initial_departure_date = cleaned_data.get('departure_date')
        initial_return_date = cleaned_data.get('return_date')
        if initial_return_date and initial_departure_date and initial_return_date < initial_departure_date:
            raise ValidationError("Return date can not be earlier than the departure date.")

        return initial

    def clean_duration(self):
        cleaned_data = super().clean()
        initial = self.cleaned_data['duration']

        if initial and initial < 1:
            raise ValidationError(
                "The duration of the stay should be equal to or greater than 1."
            )

        initial_departure_date = cleaned_data.get('departure_date')
        initial_return_date = cleaned_data.get('return_date')

        initial_duration = cleaned_data.get('duration')
        trip_duration = None

        if initial_return_date and initial_departure_date:
            trip_duration = initial_return_date - initial_departure_date

        if initial_duration and trip_duration and initial_duration > trip_duration.days:
            raise ValidationError(
                "The duration of the stay can not be longer than the period between the departure and the return dates."
            )
        return initial

    def clean_description(self):
        # Each sentence will start with Uppercase
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean_description_short(self):
        # Each sentence will start with Uppercase
        initial = self.cleaned_data['description_short']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)


class TripForm(TripModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'] = CharField(max_length=7, min_length=7)
        self.fields['duration'] = FloatField(min_value=1, step_size=1)
        self.fields['adult_price'] = FloatField(min_value=0, step_size=1)
        self.fields['child_price'] = FloatField(min_value=0, step_size=1)
        self.fields['adult_places'] = FloatField(min_value=0)
        self.fields['child_places'] = FloatField(min_value=0)

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

        self.fields['adult_price'] = FloatField()
        self.fields['child_price'] = FloatField()
        self.fields['total_price'] = FloatField()

        self.fields['total_adult_price'] = FloatField(
            widget=calculation.FormulaInput('adult_price*amount_adult')
        )
        self.fields['total_child_price'] = FloatField(
            widget=calculation.FormulaInput('child_price*amount_child')
        )
        self.fields['total_price'] = FloatField(
            widget=calculation.FormulaInput('total_adult_price+total_child_price')
        )

        for field_name in self.fields:
            if field_name in ['total_adult_price', 'total_child_price', 'total_price']:
                self.fields[field_name].widget.attrs['readonly'] = 'readonly'
                self.fields[field_name].widget.attrs['type'] = 'number'
                self.fields[field_name].widget.attrs['class'] = 'form-control-plaintext'
                self.fields[field_name].widget.attrs['style'] = 'text-align: right;'
                self.fields[field_name].initial = '0'
            else:
                self.fields[field_name].widget.attrs['class'] = 'form-control'

    def clean_firstname(self):
        """ Corrects the firstname so as it begins with capital letter. """
        initial = self.cleaned_data['firstname']
        print(f"Initial = '{initial}'")
        result = initial
        if initial:
            result = initial.capitalize()
            print(f"result  = '{result}'")
        return result

    def clean_lastname(self):
        """ Corrects the lastname so as it begins with capital letter. """
        initial = self.cleaned_data['lastname']
        print(f"Initial = '{initial}'")
        result = initial
        if initial:
            result = initial.capitalize()
            print(f"result  = '{result}'")
        return result

    def clean_birth_date(self):
        initial = self.cleaned_data['birth_date']
        print(f"Initial = '{initial}'")
        if initial > datetime.date.today():
            raise ValidationError("It is possible to set the date of birth in the past only.")
        return initial


class ContinentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = 'tady bude trip'

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
