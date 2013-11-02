from datetime import date
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from dayjournal.models import DayJournal, CashPayment, CashSales, CashPurchase, CashReceipt, CardSales, \
    CreditExpense, CreditIncome, CreditPurchase, CreditSales, ChequePurchase, LottoDetail, \
    CashEquivalentSales, SummaryInventory, SummaryTransfer, InventoryFuel, SalesAttachment, PurchaseAttachment, \
    BankAttachment, OtherAttachment
from ledger.models import Account, set_transactions, delete_rows
from inventory.models import InventoryAccount
from inventory.models import set_transactions as set_inventory_transactions
from dayjournal.serializers import DayJournalSerializer
from acubor.lib import invalid, save_model, all_empty, add


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
        day_journal = DayJournal(date=journal_date, company=request.company, sales_tax=0, cheque_deposit=0,
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
    })


@login_required
def get_journal(request):
    journal, created = DayJournal.objects.get_or_create(date=json.loads(request.body).get('day_journal_date'),
                                                        company=request.company, defaults={'sales_tax': 0,
                                                                                           'cheque_deposit': 0,
                                                                                           'cash_deposit': 0,
                                                                                           'cash_withdrawal': 0,
                                                                                           'cash_actual': 0})
    # if created:
    #     journal.save()
    return journal


@login_required
def save_cash_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashSales
    day_journal = get_journal(request)
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
    sales_tax_account = Account.objects.get(name='Sales Tax', company=request.company)
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
        tax_amount = float(row.get('tax_rate')) / 100 * float(row.get('amount'))
        net_amount = float(row.get('amount')) - tax_amount

        #sales-cr;tax-cr;cash-dr

        if tax_amount == 0:
            set_transactions(submodel, day_journal.date,
                             ['dr', cash_account, row.get('amount')],
                             ['cr', Account.objects.get(id=row.get('account_id')), net_amount],
                             # ['cr', sales_tax_account, tax_amount],
            )
        else:
            set_transactions(submodel, day_journal.date,
                             ['dr', cash_account, row.get('amount')],
                             ['cr', Account.objects.get(id=row.get('account_id')), net_amount],
                             ['cr', sales_tax_account, tax_amount],
            )
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_cash_purchase(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashPurchase
    day_journal = get_journal(request)
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'purchase_ledger_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
            #cash-cr;purchase-dr
        set_transactions(submodel, day_journal.date,
                         ['cr', cash_account, row.get('amount')],
                         ['dr', Account.objects.get(id=row.get('account_id')), row.get('amount')],
        )
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_cash_payment(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashPayment
    day_journal = get_journal(request)
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'payment_to_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
        #cash-cr;payment-dr
        set_transactions(submodel, day_journal.date,
                         ['cr', cash_account, row.get('amount')],
                         ['dr', Account.objects.get(id=row.get('account_id')), row.get('amount')],
        )
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_cash_receipt(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashReceipt
    day_journal = get_journal(request)
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'received_from_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
        #cash-dr;r_from-cr
        set_transactions(submodel, day_journal.date,
                         ['dr', cash_account, row.get('amount')],
                         ['cr', Account.objects.get(id=row.get('account_id')), row.get('amount')],
        )
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_credit_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CreditSales
    sales_tax_account = Account.objects.get(name='Sales Tax', company=request.company)
    day_journal = get_journal(request)
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_cr_id', 'account_dr_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'sales_ledger_id': row.get('account_cr_id'), 'customer_id': row.get('account_dr_id'),
                  'amount': row.get('amount'), 'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
        #sales-cr;customer-dr
        if row.get('tax_rate') is None:
            row['tax_rate'] = 0
        tax_amount = float(row.get('tax_rate')) / 100 * float(row.get('amount'))
        net_amount = float(row.get('amount')) - tax_amount
        # set_transactions(submodel, day_journal.date,
        #                  ['dr', Account.objects.get(id=row.get('account_dr_id')), row.get('amount')],
        #                  ['cr', Account.objects.get(id=row.get('account_cr_id')), row.get('amount')],
        # )
        if tax_amount == 0:
            set_transactions(submodel, day_journal.date,
                             ['dr', Account.objects.get(id=row.get('account_dr_id')), net_amount],
                             ['cr', Account.objects.get(id=row.get('account_cr_id')), net_amount],
                             # ['cr', sales_tax_account, tax_amount],
            )
        else:
            set_transactions(submodel, day_journal.date,
                             ['dr', Account.objects.get(id=row.get('account_dr_id')), net_amount],
                             ['cr', Account.objects.get(id=row.get('account_cr_id')), net_amount],
                             ['cr', sales_tax_account, tax_amount],
            )
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_credit_purchase(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CreditPurchase
    day_journal = get_journal(request)
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_cr_id', 'account_dr_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'purchase_ledger_id': row.get('account_dr_id'),
                  'supplier_id': row.get('account_cr_id'),
                  'amount': row.get('amount'), 'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
            #purchase-dr, vendor-cr
        set_transactions(submodel, day_journal.date,
                         ['dr', Account.objects.get(id=row.get('account_dr_id')), row.get('amount')],
                         ['cr', Account.objects.get(id=row.get('account_cr_id')), row.get('amount')],
        )
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_credit_income(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CreditIncome
    day_journal = get_journal(request)
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_cr_id', 'account_dr_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'income_head_id': row.get('account_cr_id'),
                  'income_from_id': row.get('account_dr_id'),
                  'amount': row.get('amount'), 'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
            # income-cr,from-dr
        set_transactions(submodel, day_journal.date,
                         ['dr', Account.objects.get(id=row.get('account_dr_id')), row.get('amount')],
                         ['cr', Account.objects.get(id=row.get('account_cr_id')), row.get('amount')],
        )
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_credit_expense(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CreditExpense
    day_journal = get_journal(request)
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_cr_id', 'account_dr_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'expense_head_id': row.get('account_dr_id'),
                  'expense_claimed_by_id': row.get('account_cr_id'),
                  'amount': row.get('amount'), 'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
            # expense_head-dr
        set_transactions(submodel, day_journal.date,
                         ['dr', Account.objects.get(id=row.get('account_dr_id')), row.get('amount')],
                         ['cr', Account.objects.get(id=row.get('account_cr_id')), row.get('amount')],
        )
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
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
        try:
            day_journal.sales_tax = row.get('register')
            day_journal.save()
            dct['saved'][0] = day_journal.id
        except:
            pass
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_summary_cash(request):
    params = json.loads(request.body)
    day_journal = get_journal(request)
    day_journal.cash_actual = params.get('rows')[0].get('actual')
    day_journal.save()
    # dct = {'invalid_attributes': {}, 'saved': {}}
    # for index, row in enumerate(params.get('rows')):
    #     invalid_attrs = invalid(row, ['register'])
    #     if invalid_attrs:
    #         dct['invalid_attributes'][index] = invalid_attrs
    #         continue
    #     day_journal = get_journal(request)
    #     try:
    #         day_journal.sales_tax = row.get('register')
    #         day_journal.save()
    #         dct['saved'][0] = day_journal.id
    #     except:
    #         pass
    return HttpResponse(json.dumps({'saved': {'0': 1}}), mimetype="application/json")


@login_required
def save_summary_transfer(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = SummaryTransfer
    day_journal = get_journal(request)
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
    card_account = Account.objects.get(name='Card Account', company=request.company)
    cheque_account = Account.objects.get(name='Cheque Account', company=request.company)
    for index, row in enumerate(params.get('rows')):
        if all_empty(row, ['cash', 'cheque', 'card']):
            continue
        for attr in ['cash', 'cheque', 'card']:
            if row.get(attr) is None or row.get(attr) == '':
                row[attr] = None
        day_journal = get_journal(request)
        values = {'sn': index + 1, 'transfer_type_id': row.get('transfer_type'), 'cash': row.get('cash'),
                  'card': row.get('card'), 'cheque': row.get('cheque'), 'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
            # Cash - Dr	; Cheque - Dr	; Bill-payment - Cr; Card - Dr
        set_transactions(submodel, day_journal.date,
                         ['dr', cash_account, row.get('cash')],
                         ['dr', card_account, row.get('card')],
                         ['dr', cheque_account, row.get('cheque')],
                         ['cr', Account.objects.get(id=row.get('transfer_type')),
                          add(row.get('cash'), row.get('card'), row.get('cheque'))],
        )
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
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
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_card_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CardSales
    day_journal = get_journal(request)
    card_account = Account.objects.get(name='Card Account', company=request.company)
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
    commission_out_account = Account.objects.get(name='Commission Out', company=request.company)
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

        net_amount = float(row.get('amount')) - float(row.get('commission_out'))
        set_transactions(submodel, day_journal.date,
                         ['dr', card_account, net_amount],
                         ['dr', commission_out_account, row.get('commission_out')],
                         ['cr', cash_account, row.get('amount')],
        )
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_cash_equivalent_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashEquivalentSales
    day_journal = get_journal(request)
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
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
        set_transactions(submodel, day_journal.date,
                         ['dr', Account.objects.get(id=row.get('account')), row.get('amount')],
                         ['cr', cash_account, row.get('amount')],
        )
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_cheque_purchase(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = ChequePurchase
    day_journal = get_journal(request)
    cheque_account = Account.objects.get(name='Cheque Account', company=request.company)
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
    commission_in_account = Account.objects.get(name='Commission In', company=request.company)
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['amount', 'commission_in'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'amount': row.get('amount'), 'commission_in': row.get('commission_in'),
                  'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        net_amount = float(row.get('amount')) - float(row.get('commission_in'))
        set_transactions(submodel, day_journal.date,
                         ['dr', cheque_account, row.get('amount')],
                         ['cr', cash_account, net_amount],
                         ['cr', commission_in_account, row.get('commission_in')],
        )
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_summary_bank(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    day_journal = get_journal(request)
    cheque_account = Account.objects.get(name='Cheque Account', company=request.company)
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
    bank_account = Account.objects.get(name='Bank Account', company=request.company)
    invalid_attrs = invalid(params.get('rows')[0], ['deposit', 'withdrawal'])
    bank_amount = 0
    cash_amount = 0
    cheque_amount = 0
    if invalid_attrs:
        dct['invalid_attributes'][0] = invalid_attrs
    else:
        day_journal.cash_deposit = params.get('rows')[0].get('deposit')
        day_journal.cash_withdrawal = params.get('rows')[0].get('withdrawal')
        bank_amount += float(params.get('rows')[0].get('deposit'))
        cash_amount -= float(params.get('rows')[0].get('deposit'))
        bank_amount -= float(params.get('rows')[0].get('withdrawal'))
        cash_amount += float(params.get('rows')[0].get('withdrawal'))
        # set_transactions(day_journal, day_journal.date,
        #                  ['dr', bank_account, params.get('rows')[0].get('deposit')],
        #                  ['cr', cash_account, params.get('rows')[0].get('deposit')],
        # )
        # set_transactions(day_journal, day_journal.date,
        #                  ['cr', bank_account, params.get('rows')[0].get('withdrawal')],
        #                  ['dr', cash_account, params.get('rows')[0].get('withdrawal')],
        # )
        dct['saved'][0] = 0
    invalid_attrs = invalid(params.get('rows')[1], ['deposit'])
    if invalid_attrs:
        dct['invalid_attributes'][1] = invalid_attrs
    else:
        day_journal.cheque_deposit = params.get('rows')[1].get('deposit')
        # set_transactions(day_journal, day_journal.date,
        #                  ['dr', bank_account, params.get('rows')[1].get('deposit')],
        #                  ['cr', cheque_account, params.get('rows')[1].get('deposit')],
        # )
        bank_amount += float(params.get('rows')[1].get('deposit'))
        cheque_amount -= float(params.get('rows')[1].get('deposit'))
        dct['saved'][1] = 1
        if cash_amount < 0:
            set_transactions(day_journal, day_journal.date, ['cr', cash_account, (-1 * cash_amount)])
        else:
            set_transactions(day_journal, day_journal.date, ['dr', cash_account, cash_amount])
        if bank_amount < 0:
            set_transactions(day_journal, day_journal.date, ['cr', bank_account, (-1 * bank_amount)])
        else:
            set_transactions(day_journal, day_journal.date, ['dr', bank_account, bank_amount])
        if cheque_amount < 0:
            set_transactions(day_journal, day_journal.date, ['cr', cheque_account, (-1 * cheque_amount)])
        else:
            set_transactions(day_journal, day_journal.date, ['dr', cheque_account, cheque_amount])
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
                                                            company=request.company, defaults={'sales_tax': 0,
                                                                                               'cheque_deposit': 0,
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
    if params.get('lotto_sales_dispenser_amount'):
        journal.lotto_sales_dispenser_amount = params.get('lotto_sales_dispenser_amount')
        journal.save()
    return HttpResponse(json.dumps({'id': journal.id}), mimetype="application/json")
