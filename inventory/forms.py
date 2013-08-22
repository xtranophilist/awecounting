from acubor.lib import KOModelForm
from django import forms
from models import Item


class ItemForm(KOModelForm):

    class Meta:
        model = Item
        exclude = ['company', 'account']
