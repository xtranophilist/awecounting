from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from ledger.models import Account

class DetailAccount(DetailView):
    model = Account

class CreateAccount(CreateView):
    model = Account
    success_url = reverse_lazy('list_account')


class ListAccount(ListView):
    model = Account


class UpdateAccount(UpdateView):
    model = Account
