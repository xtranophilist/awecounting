# from django.shortcuts import render
import json

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse

from models import Item

from serializers import ItemSerializer


class DetailItem(DetailView):
    model = Item


class CreateItem(CreateView):
    model = Item
    success_url = reverse_lazy('list_items')


class ListItem(ListView):
    model = Item


class UpdateItem(UpdateView):
    model = Item


def items_as_json(request):
    items = Item.objects.all()
    items_data = ItemSerializer(items).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")
