import json
from datetime import date
from django.db.models import Q

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from ledger.models import Account, JournalEntry, Category, Party, set_transactions
from ledger.serializers import AccountSerializer, PartySerializer, CashVendorSerializer
from forms import AccountForm, CategoryForm, PartyForm


@login_required
def accounts_as_json(request):
    accounts = Account.objects.filter(company=request.company)
    items_data = AccountSerializer(accounts).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


@login_required
def accounts_by_day_as_json(request, day):
    accounts = Account.objects.filter(company=request.company)
    items_data = AccountSerializer(accounts, day=day).data
    # items_data = AccountSerializer(accounts).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


@login_required
def customers_as_json(request):
    objs = Party.objects.filter(company=request.company, customer_account__isnull=False)
    objs_data = PartySerializer(objs).data
    return HttpResponse(json.dumps(objs_data), mimetype="application/json")


@login_required
def suppliers_as_json(request):
    objs = Party.objects.filter(company=request.company, supplier_account__isnull=False)
    objs_data = PartySerializer(objs).data
    return HttpResponse(json.dumps(objs_data), mimetype="application/json")


@login_required
def payheads_as_json(request):
    objs = Account.objects.filter(company=request.company, category__name='Pay Head')
    objs_data = AccountSerializer(objs).data
    return HttpResponse(json.dumps(objs_data), mimetype="application/json")


@login_required
def account_form(request, id=None):
    obd = Account.objects.get(name='Opening Balance Difference', company=request.company)
    if id:
        account = get_object_or_404(Account, id=id, company=request.company)
        scenario = 'Update'
    else:
        account = Account()
        scenario = 'Create'
    for query in request.GET:
        setattr(account, query, request.GET[query])
    if request.POST:
        form = AccountForm(data=request.POST, instance=account, company=request.company, scenario=scenario)
        if form.is_valid():
            opening_dr = form.cleaned_data.get('opening_dr')
            opening_cr = form.cleaned_data.get('opening_cr')
            item = form.save(commit=False)
            item.company = request.company
            item.save()
            form.save_m2m()
            if scenario == 'Create' or scenario == 'Update':
                if not opening_dr == 0:
                    set_transactions(item, date.today(),
                                     ['dr', item, form.cleaned_data['opening_dr']])
                    set_transactions(item, date.today(),
                                     ['cr', obd, form.cleaned_data['opening_dr']])
                if not opening_cr == 0:
                    set_transactions(item, date.today(),
                                     ['cr', item, form.cleaned_data['opening_cr']])
                    set_transactions(item, date.today(),
                                     ['dr', obd, form.cleaned_data['opening_cr']])
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': AccountSerializer(item).data})
            return redirect('/ledger/')
    else:
        form = AccountForm(instance=account, company=request.company, scenario=scenario)
        form.hide_field(request)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'account_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })


@login_required
def list_accounts(request):
    objects = Account.objects.filter(company=request.company)
    return render(request, 'list_accounts.html', {'accounts': objects})


@login_required
def list_all_parties(request):
    objects = Party.objects.filter(company=request.company)
    return render(request, 'list_all_parties.html', {'objects': objects})


@login_required
def view_account(request, id):
    account = get_object_or_404(Account, id=id, company=request.company)
    # transactions = account.transactions
    base_template = 'dashboard.html'
    journal_entries = JournalEntry.objects.filter(transactions__account_id=account.id).order_by('id',
                                                                                                'date') \
        .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
    return render(request, 'view_account.html', {
        'account': account,
        # 'transactions': transactions.all(),
        'journal_entries': journal_entries,
        'base_template': base_template,
    })


@login_required
def list_categories(request):
    categories = Category.objects.filter(company=request.company)
    return render(request, 'list_categories.html', {'categories': categories})


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
                return render(request, 'callback.html', {'obj': {'id': category.id, 'name': str(category)}})
            return redirect('/ledger/categories/')
    else:
        form = CategoryForm(instance=category, company=request.company)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'category_create_form.html', {
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
            return redirect('/ledger/categories/')
    else:
        form = CategoryForm(instance=category, company=request.company)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'category_update_form.html', {
        'form': form,
        'base_template': base_template
    })


@login_required
def delete_category(request, id):
    category = get_object_or_404(Category, id=id, company=request.company)
    category.delete()
    return redirect('/ledger/categories/')


@login_required
def delete_account(request, id):
    obj = get_object_or_404(Account, id=id, company=request.company)
    obj.delete()
    return redirect('/ledger/')


@login_required
def delete_party(request, id):
    object = get_object_or_404(Party, id=id, company=request.company)
    object.delete()
    return redirect('/ledger/parties/')


@login_required
def party_form(request, id=None):
    if id:
        scenario = 'Update'
        party = get_object_or_404(Party, id=id, company=request.company)
    else:
        scenario = 'Create'
        party = Party()
    for query in request.GET:
        setattr(party, query, request.GET[query])
    if request.POST:
        form = PartyForm(data=request.POST, instance=party)
        if form.is_valid():
            party = form.save(commit=False)
            party.company = request.company
            party.save()
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': PartySerializer(party).data})
            redirect('/ledger/parties')
    else:
        form = PartyForm(instance=party)
        for query in request.GET:
            form.fields[query].widget = form.fields[query].hidden_widget()
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'party_form.html', {
        'form': form,
        'scenario': scenario,
        'base_template': base_template,
    })


@login_required
def cash_and_vendors(request):
    objs = Account.objects.filter(Q(category__name="Cash Account") | Q(category__name="Suppliers")).filter(
        company=request.company)
    objs_data = CashVendorSerializer(objs).data
    return HttpResponse(json.dumps(objs_data), mimetype="application/json")


@login_required
def fixed_assets(request):
    objs = Account.objects.filter(category__name='Fixed Assets', company=request.company)
    objs_data = AccountSerializer(objs).data
    return HttpResponse(json.dumps(objs_data), mimetype="application/json")