# File: forms.py
#from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms
from .models import Reserve

class CreateForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(CreateForm, self).clean()
        table = cleaned_data.get("table")
        person = cleaned_data.get("person")

        if person>table.category.max_person:
            raise forms.ValidationError("Table %s con only contain %d diners"%(table, table.category.max_person))
        if person<table.category.min_person:
            raise forms.ValidationError("Table %s should have at least %d diners"%(table, table.category.min_person))

    class Meta:
        model = Reserve
        fields = ['custom', 'date', 'hour', 'person', 'table']#['custom', 'person']#