from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

INVITATIONCODE = "HUXINJAY"

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    vcode = forms.CharField(max_length=30, help_text='Ivitation Code')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'vcode', 'password1', 'password2', )

    def is_valid(self):
        valid = super(SignUpForm, self).is_valid()
        return ((self.cleaned_data['vcode']==INVITATIONCODE) and valid)
