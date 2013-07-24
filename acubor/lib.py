from django.forms import ModelForm

class KOModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(KOModelForm, self).__init__(*args, **kwargs)
        self.refine()

    def refine(self):
        for (name, field) in self.fields.items():
            # add HTML5 required attribute for required fields
            if field.required:
                field.widget.attrs['required'] = 'required'
            field.widget.attrs['data-bind'] = 'value: '+name

