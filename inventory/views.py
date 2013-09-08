import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from models import Item, InventoryAccount, Category
from serializers import ItemSerializer, InventoryAccountSerializer
from forms import ItemForm, CategoryForm
from inventory.filters import InventoryItemFilter


@login_required
def accounts_as_json(request):
    accounts = InventoryAccount.objects.filter(company=request.user.company)
    items_data = InventoryAccountSerializer(accounts).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


@login_required
def accounts_by_day_as_json(request, day):
    accounts = InventoryAccount.objects.filter(company=request.user.company)
    items_data = InventoryAccountSerializer(accounts, day=day).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


@login_required
def item_form(request, id=None):
    if id:
        item = get_object_or_404(Item, id=id, company=request.user.company)
        scenario = 'Update'
    else:
        item = Item()
        scenario = 'Create'
    if request.POST:
        form = ItemForm(data=request.POST, instance=item, company=request.user.company)
        if form.is_valid():
            item = form.save(commit=False)
            item.company = request.user.company
            item.save()
            return redirect('/inventory/items/')
    else:
        form = ItemForm(instance=item, company=request.user.company)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'item_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })


@login_required
def delete_inventory_item(request, id):
    object = get_object_or_404(Item, id=id, company=request.user.company)
    object.delete()
    return redirect('/inventory/items/')


@login_required
def items_as_json(request):
    items = Item.objects.filter(company=request.user.company)
    items_data = ItemSerializer(items).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


@login_required
def list_all_items(request):
    objects = Item.objects.filter(company=request.user.company)
    filtered_items = InventoryItemFilter(request.GET, queryset=objects, company=request.user.company)
    return render(request, 'list_all_items.html', {'objects': filtered_items})


@login_required
def list_categories(request):
    categories = Category.objects.filter(company=request.user.company)
    return render(request, 'list_inventory_categories.html', {'categories': categories})


@login_required
def create_category(request):
    category = Category()
    if request.POST:
        form = CategoryForm(data=request.POST, company=request.user.company)
        if form.is_valid():
            category = form.save(commit=False)
            category.company = request.user.company
            category.save()
            return redirect('/inventory/categories/')
    else:
        form = CategoryForm(instance=category, company=request.user.company)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'inventory_category_create_form.html', {
        'form': form,
        'base_template': base_template,
    })


@login_required
def update_category(request, id):
    category = get_object_or_404(Category, id=id, company=request.user.company)
    if request.POST:
        form = CategoryForm(data=request.POST, instance=category, company=request.user.company)
        if form.is_valid():
            category = form.save(commit=False)
            category.company = request.user.company
            category.save()
            return redirect('/inventory/categories/')
    else:
        form = CategoryForm(instance=category, company=request.user.company)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'inventory_category_update_form.html', {
        'form': form,
        'base_template': base_template
    })


@login_required
def delete_category(request, id):
    category = get_object_or_404(Category, id=id, company=request.user.company)
    category.delete()
    return redirect('/inventory/categories/')
