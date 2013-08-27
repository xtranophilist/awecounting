from django.shortcuts import render, get_object_or_404
from dayjournal.models import DayJournal, CashPayment, CashSales, CashPurchase, CashReceipt, CardSales, \
    CreditExpense, CreditIncome, CreditPurchase, CreditSales, LottoDetailRow, ChequePurchase, \
    CashEquivalentSales, SummaryBank, SummaryCash, SummaryInventory, SummaryTransfer, SummaryLotto
from ledger.models import Transaction, Account

from datetime import date
from dayjournal.serializers import DayJournalSerializer, DayJournalLottoSerializer
from django.http import HttpResponse
import json
from acubor.lib import delete_rows, invalid, save_model, all_empty, dr, cr, set_transactions


def day_journal(request, journal_date=None):
    if journal_date:
        day_journal = get_object_or_404(DayJournal, date=journal_date)
    else:
        day_journal, created = DayJournal.objects.get_or_create(date=date.today(), defaults={
            'company': request.user.company, 'sales_tax': 0, 'cheque_deposit': 0, 'cash_deposit': 0,
            'cash_withdrawal': 0})
    day_journal_data = DayJournalSerializer(day_journal).data
    base_template = 'dashboard.html'
    return render(request, 'day_journal.html', {
        'day_journal': day_journal_data,
        'base_template': base_template,
    })


def get_journal(request):
    journal, created = DayJournal.objects.get_or_create(date=json.loads(request.body).get('day_journal_date'),
                                                        company=request.user.company)
    if created:
        journal.save()
    return journal


def save_cash_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashSales
    cash_account = Account.objects.get(name='Cash', company=request.user.company)
    for index, row in enumerate(params.get('rows')):
        day_journal = get_journal(request)
        invalid_attrs = invalid(row, ['account_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'sales_ledger_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)

        #sales-cr;cash-dr
        set_transactions(submodel,
                         dr(cash_account, row.get('amount'), day_journal.date),
                         cr(Account.objects.get(id=row.get('account_id')), row.get('amount'), day_journal.date),
        )

        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_cash_purchase(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashPurchase
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'purchase_ledger_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        #cash-cr;purchase-dr
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_cash_payment(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashPayment
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'payment_to_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
        #cash-cr;payment-dr
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_cash_receipt(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashReceipt
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'received_from_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
        #cash-dr;r_from-cr
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_credit_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CreditSales
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_cr_id', 'account_dr_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'sales_ledger_id': row.get('account_cr_id'), 'customer_id': row.get('account_dr_id'),
                  'amount': row.get('amount'), 'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
        #sales-cr;customer-dr
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_credit_purchase(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CreditPurchase
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_cr_id', 'account_dr_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'purchase_ledger_id': row.get('account_dr_id'),
                  'supplier_id': row.get('account_cr_id'),
                  'amount': row.get('amount'), 'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_credit_income(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CreditIncome
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_cr_id', 'account_dr_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'income_head_id': row.get('account_dr_id'),
                  'income_from_id': row.get('account_cr_id'),
                  'amount': row.get('amount'), 'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_credit_expense(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CreditExpense
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_cr_id', 'account_dr_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'expense_head_id': row.get('account_cr_id'),
                  'expense_claimed_by_id': row.get('account_dr_id'),
                  'amount': row.get('amount'), 'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


# def save_summary_equivalent(request):
#     params = json.loads(request.body)
#     # print params
#     dct = {'invalid_attributes': {}, 'saved': {}}
#     model = SummaryEquivalent
#
#     #saving summary_cash
#     invalid_attrs = invalid(params.get('summary_cash'), ['actual'])
#     if not invalid_attrs:
#         values = {'actual': params.get('summary_cash').get('actual'), 'day_journal': get_journal(request)}
#         summary_cash, created = SummaryCash.objects.get_or_create(id=params.get('summary_cash').get('id'), defaults=values)
#         if not created:
#             summary_cash = save_model(summary_cash, values)
#         dct['saved'][0] = summary_cash.id
#
#     #saving cash equivalent rows
#     for index, row in enumerate(params.get('rows')):
#         invalid_attrs = invalid(row, ['account_id'])
#         if invalid_attrs:
#             dct['invalid_attributes'][index] = invalid_attrs
#             continue
#         for attr in ['inward', 'outward', 'actual']:
#             if row.get(attr) is None or row.get(attr) == '':
#                 print attr
#                 row[attr] = 0
#         values = {'sn': index+2, 'particular_id': row.get('account_id'), 'inward': row.get('inward'),
#                   'outward': row.get('outward'), 'actual': row.get('actual'), 'day_journal': get_journal(request)}
#         submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
#         if not created:
#             submodel = save_model(submodel, values)
#         dct['saved'][index+1] = submodel.id
#     delete_rows(params.get('deleted_rows'), model)
#     return HttpResponse(json.dumps(dct), mimetype="application/json")


# def save_summary_bank(request):
#     params = json.loads(request.body)
#     dct = {'invalid_attributes': {}, 'saved': {}}
#     model = SummaryBank
#     for index, row in enumerate(params.get('rows')):
#         print row
#         invalid_attrs = invalid(row, ['bank_account'])
#         if invalid_attrs:
#             dct['invalid_attributes'][index] = invalid_attrs
#             continue
#         values = {'sn': index+1, 'bank_account_id': row.get('bank_account'),
#                   'cheque_deposit': row.get('cheque_deposit'),
#                   'cash_deposit': row.get('cash_deposit'), 'day_journal': get_journal(request)}
#         submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
#         if not created:
#             submodel = save_model(submodel, values)
#         dct['saved'][index] = submodel.id
#     delete_rows(params.get('deleted_rows'), model)
#     return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_summary_sales_tax(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    for index, row in enumerate(params.get('rows')):
        print row
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


def save_summary_lotto(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = SummaryLotto
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['particular', 'disp', 'reg'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'particular_id': row.get('particular'),
                  'disp': row.get('disp'),
                  'reg': row.get('reg'), 'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_summary_transfer(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}

    #saving summary_utility
    # invalid_attrs = invalid(params.get('summary_utility'), ['amount'])
    # if not invalid_attrs:
    #     values = {'amount': params.get('summary_utility').get('amount'), 'day_journal': get_journal(request)}
    # summary_utility, created = SummaryUtility.objects.get_or_create(
    #     id=params.get('summary_utility').get('id'),
    #     defaults=values
    # )
    # if not created:
    #     summary_utility = save_model(summary_utility, values)
    # dct['saved'][0] = summary_utility.id

    #saving summary transfer rows
    model = SummaryTransfer
    for index, row in enumerate(params.get('rows')):

        if all_empty(row, ['cash', 'cheque', 'card']):
            continue

        for attr in ['cash', 'cheque', 'card']:
            if row.get(attr) is None or row.get(attr) == '':
                row[attr] = 0

        values = {'sn': index + 1, 'transfer_type_id': row.get('transfer_type'), 'cash': row.get('cash'),
                  'card': row.get('card'), 'cheque': row.get('cheque'), 'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_summary_inventory(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = SummaryInventory
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_id', 'inward', 'outward', 'actual'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'purchase': row.get('inward'), 'particular_id': row.get('account_id'),
                  'sales': row.get('outward'), 'actual': row.get('actual'), 'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def lotto_detail(request, journal_date=None):
    if journal_date:
        day_journal = get_object_or_404(DayJournal, date=journal_date)
    else:
        day_journal, created = DayJournal.objects.get_or_create(date=date.today(), company=request.user.company)
    day_journal_data = DayJournalLottoSerializer(day_journal).data
    base_template = 'dashboard.html'
    return render(request, 'day_lotto.html', {
        'day_journal': day_journal_data,
        'base_template': base_template,
    })


def save_lotto_detail(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = LottoDetailRow
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['type', 'purchase_pack', 'purchase_quantity', 'sold_quantity', 'actual_quantity'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'type_id': row.get('type'), 'purchase_pack': row.get('purchase_pack'),
                  'purchase_quantity': row.get('purchase_quantity'), 'sold_quantity': row.get('sold_quantity'),
                  'rate': row.get('rate'),
                  'actual_quantity': row.get('actual_quantity'), 'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_card_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CardSales
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['amount', 'commission_out'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'amount': row.get('amount'), 'commission_out': row.get('commission_out'),
                  'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_cash_equivalent_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashEquivalentSales
    for index, row in enumerate(params.get('rows')):
        print row
        invalid_attrs = invalid(row, ['amount', 'account'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'amount': row.get('amount'), 'account_id': row.get('account'),
                  'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_cheque_purchase(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = ChequePurchase
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['amount', 'commission_in'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'amount': row.get('amount'), 'commission_in': row.get('commission_in'),
                  'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_summary_bank(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    day_journal = get_journal(request)
    invalid_attrs = invalid(params.get('rows')[0], ['deposit', 'withdrawal'])
    print params.get('rows')
    if invalid_attrs:
        dct['invalid_attributes'][0] = invalid_attrs
    else:
        day_journal.cash_deposit = params.get('rows')[0].get('deposit')
        day_journal.cash_withdrawal = params.get('rows')[0].get('withdrawal')
        dct['saved'][0] = 0
    invalid_attrs = invalid(params.get('rows')[1], ['deposit'])
    if invalid_attrs:
        dct['invalid_attributes'][1] = invalid_attrs
    else:
        day_journal.cheque_deposit = params.get('rows')[1].get('deposit')
        dct['saved'][1] = 1
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")