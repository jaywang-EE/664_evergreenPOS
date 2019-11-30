# File: forms.py
#from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms
from reserve.models import Table
from .models import Order

class CreateForm(forms.ModelForm):
    '''
    def __init__(self, n=None, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        self.table = kwargs['initial']['table']
    '''
    def clean(self) :
        cleaned_data = super().clean()
        #person = cleaned_data.get('person')
    
    class Meta:
        model = Order
        fields = ['custom','phone','addr']
