import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from models import Item
from serializers import ItemSerializer
from forms import ItemForm


def item_form(request, id=None):
    if id:
        item = get_object_or_404(Item, id=id)
    else:
        item = Item()
    if request.POST:
        form = ItemForm(data=request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.company = request.user.company
            item.save()
    else:
        form = ItemForm(instance=item)
    base_template = 'dashboard.html'
    return render(request, 'item_form.html', {
        'form': form,
        'base_template': base_template,
    })

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
