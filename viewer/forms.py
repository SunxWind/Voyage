import re

from django.core.exceptions import ValidationError
from django.forms import (
  CharField, DateField, Form, ModelForm, IntegerField, ModelChoiceField, Textarea, TextInput, EmailInput, PasswordInput, ModelForm, DateInput, NumberInput
)

from viewer.models import Hotel, Airport, Trip  # Country
from django.contrib.auth.forms import UserCreationForm

class TripModelForm(ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'

    # def clean_description(self):
    #     # Each sentence will start with Uppercase
    #     initial = self.cleaned_data['description']
    #     sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
    #     return '. '.join(sentence.capitalize() for sentence in sentences)

    # def clean(self):
    #     result = super().clean()
    #     if result['genre'].name == 'commedy' and result['rating'] > 5:
    #         self.add_error('genre', '')
    #         self.add_error('rating', '')
    #         raise ValidationError(
    #             "Commedies aren't so good to be rated over 5."
    #         )
    #     return result

class TripForm(TripModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'