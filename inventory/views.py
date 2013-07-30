from django.shortcuts import render
import json

from django.http import HttpResponse

from models import Item

from serializers import ItemSerializer
from forms import ItemForm


def item_form(request):
    item = Item()
    form = ItemForm(data=request.POST, instance=item)
    if request.POST:
        if form.is_valid():
            item = form.save(commit=False)
            item.company = request.user.company
            item.save()
    return render(request, 'item_form.html', {'form': form})

# class DetailItem(DetailView):
#     model = Item
#
#
# class CreateItem(CreateView):
#     model = Item
#     success_url = reverse_lazy('list_items')
#
#
# class ListItem(ListView):
#     model = Item
#
#
# class UpdateItem(UpdateView):
#     model = Item


def items_as_json(request):
    items = Item.objects.all()
    items_data = ItemSerializer(items).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")
