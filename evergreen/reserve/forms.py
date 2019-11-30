# File: forms.py
#from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms
from reserve.models import Table
from .models import Reserve

class CreateForm(forms.ModelForm):
    '''
    def __init__(self, *args, **kwargs):
        #using kwargs
        self.tb = kwargs.pop('table', None)
        super(CreateForm, self).__init__(*args, **kwargs)
        #self.fields['table'].queryset = User.objects.filter(pk = user.id)
    '''

    def __init__(self, n=None, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        self.table = kwargs['initial']['table']

    def clean(self) :
        cleaned_data = super().clean()
        person = cleaned_data.get('person')
        if person>self.table.category.max_person:
            raise forms.ValidationError("Table %s con only contain %d diners"%(self.table, self.table.category.max_person))
        if person<self.table.category.min_person:
            raise forms.ValidationError("Table %s should have at least %d diners"%(self.table, self.table.category.min_person))

    class Meta:
        model = Reserve
        fields = ['custom', 'person', 'phone']
