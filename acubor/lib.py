import os
from django import forms
from ledger.models import JournalEntry, Transaction
from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.db import connection


class ExtFileField(forms.FileField):
    """
    Same as forms.FileField, but you can specify a file extension whitelist.

    Traceback (most recent call last):
    ...
    ValidationError: [u'Not allowed filetype!']
    """

    def __init__(self, *args, **kwargs):
        ext_whitelist = kwargs.pop("ext_whitelist")
        self.ext_whitelist = [i.lower() for i in ext_whitelist]

        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ExtFileField, self).clean(*args, **kwargs)
        if data is None:
            if self.required:
                raise forms.ValidationError("This file is required")
            else:
                return
        elif data is not False:
            filename = data.name
            ext = os.path.splitext(filename)[1]
            ext = ext.lower()
            if ext not in self.ext_whitelist:
                file_types = ", ".join([i for i in self.ext_whitelist])
                error = "Only allowed file types are: %s" % file_types
                raise forms.ValidationError(error)


class KOModelForm(forms.ModelForm):
    class EmailTypeInput(forms.widgets.TextInput):
        input_type = 'email'

    class NumberTypeInput(forms.widgets.TextInput):
        input_type = 'number'

    class TelephoneTypeInput(forms.widgets.TextInput):
        input_type = 'tel'

    class DateTypeInput(forms.widgets.DateInput):
        input_type = 'date'

    class DateTimeTypeInput(forms.widgets.DateTimeInput):
        input_type = 'datetime'

    class TimeTypeInput(forms.widgets.TimeInput):
        input_type = 'time'

    def __init__(self, *args, **kwargs):
        super(KOModelForm, self).__init__(*args, **kwargs)
        self.refine()

    def refine(self):
        for (name, field) in self.fields.items():
            # add HTML5 required attribute for required fields
            if field.required:
                field.widget.attrs['required'] = 'required'
            field.widget.attrs['data-bind'] = 'value: ' + name


def invalid(row, required_fields):
    invalid_attrs = []
    for attr in required_fields:
        # if one of the required attributes isn't received or is an empty string
        if not attr in row or row.get(attr) == "":
            invalid_attrs.append(attr)
    if len(invalid_attrs) is 0:
        return False
    return invalid_attrs


def all_empty(row, required_fields):
    empty = True
    for attr in required_fields:
        # if one of the required attributes isn received or is not an empty string
        if attr in row and row.get(attr) != "":
            empty = False
    return empty


def save_model(model, values):
    for key, value in values.items():
        setattr(model, key, value)
    model.save()
    return model


def delete_rows(rows, model):
    for row in rows:
        if row.get('id'):
            instance = model.objects.get(id=row.get('id'))
            JournalEntry.objects.get(content_type=ContentType.objects.get_for_model(model),
                                     model_id=instance.id).delete()
            instance.delete()


def dr(account, amount):
    if amount is None:
        return
    transaction = Transaction(account=account, dr_amount=amount)
    return transaction


def cr(account, amount, date):
    if amount is None:
        return
    transaction = Transaction(account=account, cr_amount=amount)
    return transaction


def zero_for_none(obj):
    if obj is None:
        return 0
    else:
        return obj


def none_for_zero(obj):
    if not obj:
        return None
    else:
        return obj


def alter(account, date, dr_difference, cr_difference):
    print 'altering for' + str(account)
    print dr_difference
    s = Transaction.objects.filter(journal_entry__date__gt=date, account=account).update(
        current_dr=none_for_zero(zero_for_none(F('current_dr')) + zero_for_none(dr_difference)),
        current_cr=none_for_zero(zero_for_none(F('current_cr')) + zero_for_none(cr_difference)))
    # print connection.queries


def set_transactions(submodel, date, *args):
    # [transaction.delete() for transaction in submodel.transactions.all()]
    # args = [arg for arg in args if arg is not None]
    journal_entry, created = JournalEntry.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(submodel), model_id=submodel.id,
        defaults={
            'date': date
        })
    for arg in args:
        # transaction = Transaction(account=arg[1], dr_amount=arg[2])
        matches = journal_entry.transactions.filter(account=arg[1])
        if not matches:
            transaction = Transaction()
            transaction.account = arg[1]
            if arg[0] == 'dr':
                transaction.dr_amount = float(arg[2])
                transaction.account.current_dr = none_for_zero(
                    zero_for_none(transaction.account.current_dr) + transaction.dr_amount)
                transaction.current_dr = transaction.account.current_dr
                alter(arg[1], date, float(arg[2]), 0)
            if arg[0] == 'cr':
                transaction.cr_amount = float(arg[2])
                transaction.account.current_cr = none_for_zero(
                    zero_for_none(transaction.account.current_cr) + transaction.cr_amount)
                transaction.current_cr = transaction.account.current_cr
                alter(arg[1], date, 0, float(arg[2]))
        else:
            transaction = matches[0]
            transaction.account = arg[1]

            # cancel out existing dr_amount and cr_amount from current_dr and current_cr
            # if transaction.dr_amount:
            #     transaction.current_dr -= transaction.dr_amount
            #     transaction.account.current_dr -= transaction.dr_amount
            #
            # if transaction.cr_amount:
            #     transaction.current_cr -= transaction.cr_amount
            #     transaction.account.current_cr -= transaction.cr_amount

            # save new dr_amount and add it to current_dr/cr
            if arg[0] == 'dr':
                dr_difference = float(arg[2]) - zero_for_none(transaction.dr_amount)
                cr_difference = zero_for_none(transaction.cr_amount) * -1
                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
                transaction.dr_amount = float(arg[2])
                transaction.cr_amount = None
            else:
                cr_difference = float(arg[2]) - zero_for_none(transaction.cr_amount)
                dr_difference = zero_for_none(transaction.dr_amount) * -1
                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
                transaction.cr_amount = float(arg[2])
                transaction.dr_amount = None

            transaction.current_dr = none_for_zero(zero_for_none(transaction.current_dr) + dr_difference)
            transaction.current_cr = none_for_zero(zero_for_none(transaction.current_cr) + cr_difference)
            transaction.account.current_dr = none_for_zero(
                zero_for_none(transaction.account.current_dr) + dr_difference)
            transaction.account.current_cr = none_for_zero(
                zero_for_none(transaction.account.current_cr) + cr_difference)

        transaction.account.save()

        journal_entry.transactions.add(transaction)


def add(*args):
    total = 0
    for arg in args:
        if arg == '':
            arg = 0
        total += float(arg)
    return total