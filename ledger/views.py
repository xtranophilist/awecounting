from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from ledger.models import Account
from ledger.serializers import AccountSerializer
from django.http import HttpResponse
import json


class DetailAccount(DetailView):
    model = Account


class CreateAccount(CreateView):
    model = Account
    success_url = reverse_lazy('list_account')


class ListAccount(ListView):
    model = Account


class UpdateAccount(UpdateView):
    model = Account


def accounts_as_json(request):
    accounts = Account.objects.all()
    items_data = AccountSerializer(accounts).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")
