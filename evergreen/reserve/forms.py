from django import forms
from reserve.models import Table
from .models import Reserve

# to validate person number
class CreateForm(forms.ModelForm):
    def clean(self) :
        cleaned_data = super().clean()
        num = cleaned_data.get('person')
        tb  = self.initial.get('table')
        err_msg = tb.valid(num)
        if err_msg: raise forms.ValidationError(err_msg)

    class Meta:
        model = Reserve
        fields = ['custom', 'person', 'phone']


