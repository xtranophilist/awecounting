from datetime import date
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from dayjournal.models import DayJournal, CashSales, CardSales, LottoDetail, BankAttachment, OtherAttachment, \
    CashEquivalentSales, SummaryInventory, SummaryTransfer, InventoryFuel, SalesAttachment, PurchaseAttachment, VendorPayout, OtherPayout
from ledger.models import Account, set_transactions, delete_rows, Category
from inventory.models import InventoryAccount
from inventory.models import set_transactions as set_inventory_transactions
from dayjournal.serializers import DayJournalSerializer, LottoDetailSerializer
from acubor.lib import invalid, save_model, all_empty, add, zero_for_none
from users.models import group_required


@login_required
def all_day_journals(request):
    objects = DayJournal.objects.filter(company=request.company)
    return render(request, 'all_day_journals.html', {'objects': objects})


@login_required
def day_journal(request, journal_date=None):
    if not journal_date:
        journal_date = date.today()
    try:
        day_journal = DayJournal.objects.get(date=journal_date, company=request.company)
    except DayJournal.DoesNotExist:
        day_journal = DayJournal(date=journal_date, company=request.company, cheque_deposit=0,
                                 cash_deposit=0, cash_withdrawal=0, cash_actual=0)
    day_journal_data = DayJournalSerializer(day_journal).data
    base_template = 'dashboard.html'
    return render(request, 'day_journal.html', {
        'day_journal': day_journal_data,
        'base_template': base_template,
        'sales_attachments': day_journal.sales_attachments.all(),
        'purchase_attachments': day_journal.purchase_attachments.all(),
        'bank_attachments': day_journal.bank_attachments.all(),
        'other_attachments': day_journal.other_attachments.all(),
        'purchase_category': Category.objects.get(name='Purchase', company=request.company)
    })


@login_required
def get_journal(request):
    params = json.loads(request.body)
    try:
        journal, created = DayJournal.objects.get_or_create(date=params.get('day_journal_date'),
                                                            company=request.company, defaults={'voucher_no': params.get(
                                                                                                   'voucher_no'),
                                                                                               'cheque_deposit': 0,
                                                                                               'cash_deposit': 0,
                                                                                               'cash_withdrawal': 0,
                                                                                               'cash_actual': 0})
    except Exception as e:
        return {'error': 'Voucher No. already exists!'}
    if not created:
        journal.voucher_no = params.get('voucher_no')
        try:
            journal.save()
        except Exception as e:
            return {'error': 'Voucher No. already exists!'}
    return journal


@login_required
def save_cash_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashSales
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'sales_ledger_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if row.get('tax_rate') is None:
            row['tax_rate'] = 0
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_summary_sales_tax(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['register'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        day_journal = get_journal(request)
        if type(day_journal) == dict:
            return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
        try:
            day_journal.sales_tax = row.get('register')
            day_journal.status = 'Unapproved'
            day_journal.save()
            dct['saved'][0] = day_journal.id
        except:
            pass
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_summary_cash(request):
    params = json.loads(request.body)
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    day_journal.cash_actual = params.get('rows')[0].get('actual')
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps({'saved': {'0': 1}}), mimetype="application/json")


@login_required
def save_summary_transfer(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = SummaryTransfer
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
    card_account = Account.objects.get(name='Card Account', company=request.company)
    cheque_account = Account.objects.get(name='Cheque Account', company=request.company)
    for index, row in enumerate(params.get('rows')):
        if all_empty(row, ['cash', 'cheque', 'card']):
            continue
        for attr in ['cash', 'cheque', 'card']:
            if row.get(attr) is None or row.get(attr) == '':
                row[attr] = None
        values = {'sn': index + 1, 'transfer_type_id': row.get('transfer_type'), 'cash': row.get('cash'),
                  'card': row.get('card'), 'cheque': row.get('cheque'), 'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_summary_inventory(request, fuel=False):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    if fuel:
        model = InventoryFuel
    else:
        model = SummaryInventory
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_id', 'purchase', 'sales', 'actual'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'purchase': row.get('purchase'), 'particular_id': row.get('account_id'),
                  'sales': row.get('sales'), 'actual': row.get('actual'), 'day_journal': day_journal}

        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        account = InventoryAccount.objects.get(id=row.get('account_id'))
        diff = float(row.get('purchase')) - float(row.get('sales'))
        if diff < 0:
            set_inventory_transactions(submodel, day_journal.date,
                                       ['cr', account, diff],
            )
        else:
            set_inventory_transactions(submodel, day_journal.date,
                                       ['dr', account, diff],
            )

        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_inventory_fuel(request):
    return save_summary_inventory(request, fuel=True)


@login_required
def save_lotto_detail(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = LottoDetail
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['rate', 'pack_count', 'day_open', 'day_close', 'addition'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'rate': row.get('rate'), 'pack_count': row.get('pack_count'),
                  'day_open': row.get('day_open'), 'day_close': row.get('day_close'),
                  'addition': row.get('addition'), 'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_card_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CardSales
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['amount', 'commission_out'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'amount': row.get('amount'), 'commission_out': row.get('commission_out'),
                  'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_cash_equivalent_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashEquivalentSales
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['amount', 'account'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'amount': row.get('amount'), 'account_id': row.get('account'),
                  'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def delete_attachment(request):
    if request.POST['type'] == 'sales':
        get_object_or_404(SalesAttachment, day_journal__company=request.company, id=request.POST['id']).delete()
    elif request.POST['type'] == 'purchase':
        get_object_or_404(PurchaseAttachment, day_journal__company=request.company, id=request.POST['id']).delete()
    elif request.POST['type'] == 'other':
        get_object_or_404(OtherAttachment, day_journal__company=request.company, id=request.POST['id']).delete()
    elif request.POST['type'] == 'bank':
        get_object_or_404(BankAttachment, day_journal__company=request.company, id=request.POST['id']).delete()
    return HttpResponse(json.dumps({'success': True}), mimetype="application/json")


@login_required
def save_attachments(request):
    if request.POST['type'] == 'sales':
        model = SalesAttachment
    elif request.POST['type'] == 'purchase':
        model = PurchaseAttachment
    elif request.POST['type'] == 'other':
        model = OtherAttachment
    elif request.POST['type'] == 'bank':
        model = BankAttachment
    captions = request.POST.getlist('captions')
    attachments = request.FILES.getlist('attachments')
    day_journal, created = DayJournal.objects.get_or_create(date=request.POST['day'],
                                                            company=request.company, defaults={'cheque_deposit': 0,
                                                                                               'cash_deposit': 0,
                                                                                               'cash_withdrawal': 0,
                                                                                               'cash_actual': 0})
    lst = []
    for i, attachment in enumerate(attachments):
        attached = model(attachment=attachment, description=captions[i], day_journal=day_journal)
        attached.save()
        lst.append(
            {'name': attachment.name, 'caption': captions[i], 'id': attached.id, 'link': attached.attachment.url})
    return HttpResponse(json.dumps(lst), mimetype="application/json")


@login_required
def save_lotto_sales_as_per_dispenser(request):
    params = json.loads(request.body)
    journal = get_journal(request)
    if type(journal) == dict:
        return HttpResponse(json.dumps({'error_message': journal['error']}), mimetype="application/json")
    if params.get('lotto_sales_dispenser_amount'):
        journal.lotto_sales_dispenser_amount = params.get('lotto_sales_dispenser_amount')
    if params.get('lotto_sales_register_amount'):
        journal.lotto_sales_register_amount = params.get('lotto_sales_register_amount')
    if params.get('scratch_off_sales_register_amount'):
        journal.scratch_off_sales_register_amount = params.get('scratch_off_sales_register_amount')
    journal.status = 'Unapproved'
    journal.save()
    journal.save()
    return HttpResponse(json.dumps({'id': journal.id}), mimetype="application/json")


@login_required
def save_vendor_payout(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = VendorPayout
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['vendor', 'amount', 'purchase_ledger', 'paid', 'type'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue

        values = {'sn': index + 1, 'vendor_id': row.get('vendor'), 'amount': row.get('amount'),
                  'purchase_ledger_id': row.get('purchase_ledger'),
                  'paid_id': row.get('paid'), 'type': row.get('type'), 'remarks': row.get('remarks'),
                  'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_other_payout(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = OtherPayout
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['paid_to', 'amount', 'paid'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'paid_to_id': row.get('paid_to'), 'amount': row.get('amount'),
                  'paid_id': row.get('paid'), 'day_journal': day_journal, 'remarks': row.get('remarks')}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def last_lotto_detail(request, journal_date):
    try:
        last_journal = DayJournal.objects.filter(date__lt=journal_date, lotto_detail__isnull=False).order_by('-date')[
            0];
        lotto_detail = last_journal.lotto_detail.all()
        lst = LottoDetailSerializer(lotto_detail).data
        return HttpResponse(json.dumps(lst), mimetype="application/json")
    except IndexError:
        return HttpResponse(json.dumps([]), mimetype="application/json")


@group_required('SuperOwner', 'Owner', 'Supervisor')
def approve(request):
    params = json.loads(request.body)
    dct = {}
    try:
        journal = DayJournal.objects.get(date=params.get('date'), company=request.company)
    except DayJournal.DoesNotExist:
        dct['error_message'] = 'Day Journal needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
    card_account = Account.objects.get(name='Card Account', company=request.company)
    total_amount = 0
    total_tax = 0
    for cash_sale in journal.cash_sales.all():
        tax_rate = cash_sale.sales_ledger.tax_rate or 0
        tax_amount = cash_sale.amount * zero_for_none(tax_rate) / 100
        net_amount = cash_sale.amount - tax_amount
        set_transactions(journal, journal.date,
                         ['cr', cash_sale.sales_ledger, net_amount],
        )
        total_amount += cash_sale.amount
        total_tax += tax_amount
    if journal.lotto_sales_dispenser_amount is None or journal.lotto_sales_dispenser_amount == 0:
        lotto_amount = journal.lotto_sales_register_amount
    else:
        lotto_amount = journal.lotto_sales_dispenser_amount
    total_amount += lotto_amount
    lotto_sales_ledger = Account.objects.get(name='Lotto Sales', company=request.company)
    lotto_tax_rate = lotto_sales_ledger.tax_rate
    lotto_tax = lotto_amount * zero_for_none(lotto_tax_rate) / 100
    net_lotto_amount = lotto_amount - lotto_tax
    total_tax += lotto_tax
    set_transactions(journal, journal.date,
                     ['cr', lotto_sales_ledger, net_lotto_amount],
    )
    scratch_off_total = 0
    for scratch_off in journal.lotto_detail.all():
        day_close = scratch_off.day_close
        if day_close == 0:
            day_close = scratch_off.pack_count
        sales = (scratch_off.pack_count * zero_for_none(scratch_off.addition) + (day_close - scratch_off.day_open)) * zero_for_none(scratch_off.rate)
        scratch_off_total += sales
    if scratch_off_total == 0:
        scratch_off_total = journal.scratch_off_sales_register_amount
    total_amount += scratch_off_total
    scratch_off_ledger = Account.objects.get(name='Scratch Off Sales', company=request.company)
    scratch_off_tax_rate = scratch_off_ledger.tax_rate
    scratch_off_tax = scratch_off_total * zero_for_none(scratch_off_tax_rate) / 100
    net_scratch_off_amount = scratch_off_total - scratch_off_tax
    total_tax += scratch_off_tax
    set_transactions(journal, journal.date,
                     ['cr', scratch_off_ledger, net_scratch_off_amount],
    )

    set_transactions(journal, journal.date,
                     ['cr', Account.objects.get(name='Sales Tax', company=request.company), total_tax],
    )

    non_cash = 0
    for card_sale in journal.card_sales.all():
        commission_out = card_sale.commission_out or 0
        net = card_sale.amount - commission_out
        set_transactions(journal, journal.date,
                         ['dr', Account.objects.get(name='Commission Out', company=request.company), commission_out],
        )
        set_transactions(journal, journal.date,
                         ['dr', card_account, net],
        )
        non_cash += card_sale.amount

    for cash_equivalent_sale in journal.cash_equivalent_sales.all():
        set_transactions(journal, journal.date,
                         ['dr', cash_equivalent_sale.account, cash_equivalent_sale.amount],
        )
        non_cash += cash_equivalent_sale.amount

    set_transactions(journal, journal.date,
                     ['dr', cash_account, total_amount - non_cash],
    )

    for row in journal.summary_transfer.all():
        # Cash - Dr	; Cheque - Dr	; Bill-payment - Cr; Card - Dr
        set_transactions(row, journal.date,
                         ['dr', cash_account, row.cash],
                         ['dr', card_account, row.card],
                         ['dr', Account.objects.get(name='Cheque Account', company=request.company), row.cheque],
                         ['cr', Account.objects.get(id=row.transfer_type), add(row.cash, row.card, row.cheque)],
        )

    for row in journal.vendor_payout.all():
        if row.type == 'new':
            set_transactions(row, journal.date,
                             ['dr', row.purchase_ledger, row.amount],
                             ['cr', row.paid, row.amount],
            )
        else:
            set_transactions(row, journal.date,
                             ['dr', row.vendor, row.amount],
                             ['cr', row.paid, row.amount],
            )

    for row in journal.other_payout.all():
        set_transactions(row, journal.date,
                         ['dr', row.paid_to, row.amount],
                         ['cr', row.paid, row.amount],
        )





    #journal.status = 'Approved'
    #journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")
