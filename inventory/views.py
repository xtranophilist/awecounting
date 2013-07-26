from django.shortcuts import render
from models import Item
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy


class DetailItem(DetailView):
    model = Item


class CreateItem(CreateView):
    model = Item
    success_url = reverse_lazy('list_items')


class ListItem(ListView):
    model = Item


class UpdateItem(UpdateView):
    model = Item

