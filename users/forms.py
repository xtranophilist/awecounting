from django import forms
from registration.forms import RegistrationForm
from registration.models import RegistrationProfile
from django.utils.translation import ugettext_lazy as _


attrs_dict = {
# 'class': 'required'
}


class UserRegistrationForm(RegistrationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
    name_of_company = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
    type_of_business = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
    location = forms.CharField(widget=forms.Textarea(attrs=attrs_dict))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    password1 = forms.CharField(max_length=32, widget=forms.PasswordInput, label=_("Password (again)"))

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['full_name', 'email','name_of_company', 'location', 'type_of_business', 'password', 'password1']

    def save(self, profile_callback=None):
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['email'])
        return new_user

    class Meta:
        # model = User
        exclude = ['username',]
