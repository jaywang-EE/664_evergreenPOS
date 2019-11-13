# File: forms.py
from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms
from .models import Reserve

class CreateForm(forms.ModelForm):
    def clean_file(self,form):
        if person<table.min_person:
            raise ValidationError(_('Invalid value'), code='invalid')
            #raise ValidationError("Table %02d should have at least %d diners"%(table.number, table.min_person))
        elif person>table.max_person:
            raise ValidationError("Table %02d con only contain %d diners"%(table.number, table.max_person))

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get("table")
        person = cleaned_data.get("person")

        if person>table.max_person:
            raise forms.ValidationError("Table %s con only contain %d diners"%(table.name, table.max_person))
        if person<table.min_person:
            raise forms.ValidationError("Table %02d should have at least %d diners"%(table.name, table.min_person))

    class Meta:
        model = Reserve
        fields = ['custom', 'date', 'hour', 'person', 'table']