from django import forms
from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
# from registration_email.forms import EmailRegistrationForm


attrs_dict = {
    # 'class': 'required'
}


class UserRegistrationForm(RegistrationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
    name_of_company = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
    type_of_business = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
    location = forms.CharField(widget=forms.Textarea(attrs=attrs_dict))
    # password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    # password1 = forms.CharField(max_length=32, widget=forms.PasswordInput, label=_("Password (again)"))

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        existing = get_user_model().objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        existing = get_user_model().objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that email already exists."))
        else:
            return self.cleaned_data['email']

    def clean_name_of_company(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        from users.models import Company
        existing = Company.objects.filter(name__iexact=self.cleaned_data['name_of_company'])
        if existing.exists():
            raise forms.ValidationError(_("The company name is already taken."))
        else:
            return self.cleaned_data['name_of_company']

        #
    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        # self.cleaned_data['username'] = self.cleaned_data['email']
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

    class Meta:
        model = get_user_model()
        # exclude = ['username',]
