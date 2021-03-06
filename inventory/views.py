import json
from django.core.urlresolvers import reverse_lazy

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ledger.models import Account

from models import Item, InventoryAccount, Category, Unit
from serializers import ItemSerializer, InventoryAccountSerializer, InventoryCategorySerializer
from forms import ItemForm, CategoryForm, UnitForm
from inventory.filters import InventoryItemFilter
from tax.models import TaxScheme


@login_required
def accounts_as_json(request):
    accounts = InventoryAccount.objects.filter(company=request.company)
    items_data = InventoryAccountSerializer(accounts).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


@login_required
def accounts_by_day_as_json(request, day):
    accounts = InventoryAccount.objects.filter(company=request.company)
    items_data = InventoryAccountSerializer(accounts, day=day).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


@login_required
def item_form(request, id=None):
    if id:
        item = get_object_or_404(Item, id=id, company=request.company)
        scenario = 'Update'
    else:
        item = Item(purchase_account=Account.objects.get(name='Purchase', company=request.company),
                    sales_account=Account.objects.get(name='Sales', company=request.company),
                    purchase_tax_scheme=TaxScheme.objects.get(name='No Tax', company=request.company),
                    sales_tax_scheme=TaxScheme.objects.get(name='No Tax', company=request.company))
        scenario = 'Create'
    if request.POST:
        form = ItemForm(data=request.POST, instance=item, company=request.company)
        if form.is_valid():
            item = form.save(commit=False)
            item.company = request.company
            item.save()
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': ItemSerializer(item).data})
            return redirect('/inventory/items/')
    else:
        form = ItemForm(instance=item, company=request.company)
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
def create_item(request):
    """
    @param request:
    @param id:
    @return: JSON for account for added Inventory Item
    """
    item = Item(purchase_account=Account.objects.get(name='Purchase', company=request.company),
                sales_account=Account.objects.get(name='Sales', company=request.company),
                purchase_tax_scheme=TaxScheme.objects.get(name='No Tax', company=request.company),
                sales_tax_scheme=TaxScheme.objects.get(name='No Tax', company=request.company))
    scenario = 'Create'
    for query in request.GET:
        setattr(item, query, request.GET[query])
    if request.POST:
        form = ItemForm(data=request.POST, instance=item, company=request.company)
        if form.is_valid():
            item = form.save(commit=False)
            item.company = request.company
            item.save()
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': InventoryAccountSerializer(item.account).data})
            return redirect('/inventory/items/')
    else:
        form = ItemForm(instance=item, company=request.company)
        form.hide_field(request)
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
    obj = get_object_or_404(Item, id=id, company=request.company)
    obj.delete()
    return redirect('/inventory/items/')


@login_required
def items_as_json(request):
    items = Item.objects.filter(company=request.company)
    items_data = ItemSerializer(items).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


@login_required
def list_all_items(request):
    objects = Item.objects.filter(company=request.company)
    filtered_items = InventoryItemFilter(request.GET, queryset=objects, company=request.company)
    return render(request, 'list_all_items.html', {'objects': filtered_items})


@login_required
def list_categories(request):
    categories = Category.objects.filter(company=request.company)
    return render(request, 'list_inventory_categories.html', {'categories': categories})


@login_required
def create_category(request):
    category = Category()
    if request.POST:
        form = CategoryForm(data=request.POST, company=request.company)
        if form.is_valid():
            category = form.save(commit=False)
            category.company = request.company
            category.save()
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': InventoryCategorySerializer(category).data})
            return redirect('/inventory/categories/')
    else:
        form = CategoryForm(instance=category, company=request.company)
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
    category = get_object_or_404(Category, id=id, company=request.company)
    if request.POST:
        form = CategoryForm(data=request.POST, instance=category, company=request.company)
        if form.is_valid():
            category = form.save(commit=False)
            category.company = request.company
            category.save()
            return redirect('/inventory/categories/')
    else:
        form = CategoryForm(instance=category, company=request.company)
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
    category = get_object_or_404(Category, id=id, company=request.company)
    category.delete()
    return redirect('/inventory/categories/')


@login_required
def unit_form(request, id=None):
    if id:
        obj = get_object_or_404(Unit, id=id, company=request.company)
        scenario = 'Update'
    else:
        obj = Unit(company=request.company)
        scenario = 'Create'
    if request.POST:
        form = UnitForm(data=request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.company = request.company
            obj.save()
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': {'name': obj.name, 'id': obj.id}})
            return redirect(reverse_lazy('list_units'))
    else:
        form = UnitForm(instance=obj)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'unit_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })


@login_required
def list_units(request):
    objs = Unit.objects.filter(company=request.company)
    return render(request, 'list_units.html', {'objects': objs})


@login_required
def delete_unit(request, id):
    obj = get_object_or_404(Unit, id=id, company=request.company)
    obj.delete()
    return redirect(reverse_lazy('list_units'))
