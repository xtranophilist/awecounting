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
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'item_form.html', {
        'form': form,
        'base_template': base_template,
    })


def items_as_json(request):
    items = Item.objects.all()
    items_data = ItemSerializer(items).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")
