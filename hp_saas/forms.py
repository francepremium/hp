from django import forms
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _

from account.forms import SignupForm as PinaxSignupForm
from account.forms import LoginEmailForm as LoginForm


class SignupForm(PinaxSignupForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    company_name = forms.CharField(required=False)
    next = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean(self):
        """ We want a single password input """
        self.cleaned_data['password_confirm'] = self.cleaned_data.get('password', None)
        return super(SignupForm, self).clean()

# We want signup form fields in a certain order
SignupForm.base_fields = SortedDict((
    ('first_name', SignupForm.base_fields['first_name']),
    ('last_name', SignupForm.base_fields['last_name']),
    ('email', SignupForm.base_fields['email']),
    ('password', SignupForm.base_fields['password']),
    ('company_name', SignupForm.base_fields['company_name']),
    ('next', SignupForm.base_fields['next']),
))
