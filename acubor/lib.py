from django.forms import ModelForm
from django.forms.widgets import TextInput, DateInput, DateTimeInput, TimeInput


class KOModelForm(ModelForm):

    class EmailTypeInput(TextInput):
        input_type = 'email'

    class NumberTypeInput(TextInput):
        input_type = 'number'

    class TelephoneTypeInput(TextInput):
        input_type = 'tel'

    class DateTypeInput(DateInput):
        input_type = 'date'

    class DateTimeTypeInput(DateTimeInput):
        input_type = 'datetime'

    class TimeTypeInput(TimeInput):
        input_type = 'time'

    def __init__(self, *args, **kwargs):
        super(KOModelForm, self).__init__(*args, **kwargs)
        self.refine()

    def refine(self):
        for (name, field) in self.fields.items():
            # add HTML5 required attribute for required fields
            if field.required:
                field.widget.attrs['required'] = 'required'
            field.widget.attrs['data-bind'] = 'value: '+name

