from django.views.generic.edit import CreateView
from ledger.models import Account


class create(CreateView):
    model = Account
