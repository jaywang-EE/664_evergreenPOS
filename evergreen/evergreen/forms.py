from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

INVITATIONCODE = "HUXINJAY"

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    vcode = forms.CharField(max_length=30, label='Ivitation Code')
    email = forms.EmailField(max_length=254)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'vcode', 'password1', 'password2', )

    def is_valid(self):
        valid = super(SignUpForm, self).is_valid()
        if self.cleaned_data['vcode']!=INVITATIONCODE:
            self.add_error("vcode", 'Ivitation code not valid!')
            return False
        return valid
