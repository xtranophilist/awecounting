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
                                                        company=request.user.company, defaults={
            'sales_tax': 0, 'cheque_deposit': 0, 'cash_deposit': 0, 'cash_withdrawal': 0})
    if created:
        journal.save()
    return journal


def save_cash_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashSales
    day_journal = get_journal(request)
    cash_account = Account.objects.get(name='Cash', company=request.user.company)
    sales_tax_account = Account.objects.get(name='Sales Tax', company=request.user.company)
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

        #sales-cr;cash-dr
        set_transactions(submodel,
                         dr(cash_account, row.get('amount'), day_journal.date),
                         cr(Account.objects.get(id=row.get('account_id')), net_amount, day_journal.date),
                         cr(sales_tax_account, tax_amount, day_journal.date),
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
    day_journal = get_journal(request)
    cash_account = Account.objects.get(name='Cash', company=request.user.company)
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
        set_transactions(submodel,
                         cr(cash_account, row.get('amount'), day_journal.date),
                         dr(Account.objects.get(id=row.get('account_id')), row.get('amount'), day_journal.date),
        )
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_cash_payment(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashPayment
    day_journal = get_journal(request)
    cash_account = Account.objects.get(name='Cash', company=request.user.company)
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
        set_transactions(submodel,
                         # cr(cash_account, row.get('amount'), day_journal.date),
                         dr(Account.objects.get(id=row.get('account_id')), row.get('amount'), day_journal.date),
        )
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_cash_receipt(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashReceipt
    day_journal = get_journal(request)
    cash_account = Account.objects.get(name='Cash', company=request.user.company)
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
        set_transactions(submodel,
                         dr(cash_account, row.get('amount'), day_journal.date),
                         cr(Account.objects.get(id=row.get('account_id')), row.get('amount'), day_journal.date),
        )
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_credit_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CreditSales
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
        set_transactions(submodel,
                         dr(Account.objects.get(id=row.get('account_dr_id')), row.get('amount'), day_journal.date),
                         cr(Account.objects.get(id=row.get('account_cr_id')), row.get('amount'), day_journal.date),
        )
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


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
        set_transactions(submodel,
                         dr(Account.objects.get(id=row.get('account_dr_id')), row.get('amount'), day_journal.date),
                         cr(Account.objects.get(id=row.get('account_cr_id')), row.get('amount'), day_journal.date),
        )
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


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
        set_transactions(submodel,
                         dr(Account.objects.get(id=row.get('account_dr_id')), row.get('amount'), day_journal.date),
                         cr(Account.objects.get(id=row.get('account_cr_id')), row.get('amount'), day_journal.date),
        )
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


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
        set_transactions(submodel,
                         dr(Account.objects.get(id=row.get('account_dr_id')), row.get('amount'), day_journal.date),
                         cr(Account.objects.get(id=row.get('account_cr_id')), row.get('amount'), day_journal.date),
        )
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
    day_journal = get_journal(request)
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['particular', 'disp', 'reg'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'particular_id': row.get('particular'),
                  'disp': row.get('disp'),
                  'reg': row.get('reg'), 'day_journal': day_journal}
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
    day_journal = get_journal(request)
    cash_account = Account.objects.get(name='Cash', company=request.user.company)
    card_account = Account.objects.get(name='Card', company=request.user.company)
    cheque_account = Account.objects.get(name='Cheque', company=request.user.company)

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
        print row
        # Cash - Dr	; Cheque - Dr	; Bill-payment - Cr; Card - Dr
        set_transactions(submodel,
                         dr(cash_account, row.get('cash'), day_journal.date),
                         dr(card_account, row.get('card'), day_journal.date),
                         dr(cheque_account, row.get('cheque'), day_journal.date),
                         cr(Account.objects.get(id=row.get('transfer_type')), row.get('cash'), day_journal.date),
                         cr(Account.objects.get(id=row.get('transfer_type')), row.get('card'), day_journal.date),
                         cr(Account.objects.get(id=row.get('transfer_type')), row.get('cheque'), day_journal.date),
        )
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_summary_inventory(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = SummaryInventory
    day_journal = get_journal(request)
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_id', 'inward', 'outward', 'actual'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'purchase': row.get('inward'), 'particular_id': row.get('account_id'),
                  'sales': row.get('outward'), 'actual': row.get('actual'), 'day_journal': day_journal}
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
    day_journal = get_journal(request)
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['type', 'purchase_pack', 'purchase_quantity', 'sold_quantity', 'actual_quantity'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'type_id': row.get('type'), 'purchase_pack': row.get('purchase_pack'),
                  'purchase_quantity': row.get('purchase_quantity'), 'sold_quantity': row.get('sold_quantity'),
                  'rate': row.get('rate'),
                  'actual_quantity': row.get('actual_quantity'), 'day_journal': day_journal}
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
    day_journal = get_journal(request)
    card_account = Account.objects.get(name='Card', company=request.user.company)
    cash_account = Account.objects.get(name='Cash', company=request.user.company)
    commission_out_account = Account.objects.get(name='Commission Out', company=request.user.company)
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
        set_transactions(submodel,
                         dr(card_account, net_amount, day_journal.date),
                         dr(commission_out_account, row.get('commission_out'), day_journal.date),
                         cr(cash_account, row.get('amount'), day_journal.date),
        )
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_cash_equivalent_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashEquivalentSales
    day_journal = get_journal(request)
    cash_account = Account.objects.get(name='Cash', company=request.user.company)
    for index, row in enumerate(params.get('rows')):
        print row
        invalid_attrs = invalid(row, ['amount', 'account'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'amount': row.get('amount'), 'account_id': row.get('account'),
                  'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        set_transactions(submodel,
                         dr(Account.objects.get(id=row.get('account')), row.get('amount'), day_journal.date),
                         cr(cash_account, row.get('amount'), day_journal.date),
        )
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_cheque_purchase(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = ChequePurchase
    day_journal = get_journal(request)
    cheque_account = Account.objects.get(name='Cheque', company=request.user.company)
    cash_account = Account.objects.get(name='Cash', company=request.user.company)
    commission_in_account = Account.objects.get(name='Commission In', company=request.user.company)
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
        set_transactions(submodel,
                         dr(cheque_account, row.get('amount'), day_journal.date),
                         cr(cash_account, net_amount, day_journal.date),
                         cr(commission_in_account, row.get('commission_in'), day_journal.date),
        )
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_summary_bank(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    day_journal = get_journal(request)
    cheque_account = Account.objects.get(name='Cheque', company=request.user.company)
    cash_account = Account.objects.get(name='Cash', company=request.user.company)
    bank_account = Account.objects.get(name='Bank', company=request.user.company)
    invalid_attrs = invalid(params.get('rows')[0], ['deposit', 'withdrawal'])
    print params.get('rows')
    if invalid_attrs:
        dct['invalid_attributes'][0] = invalid_attrs
    else:
        day_journal.cash_deposit = params.get('rows')[0].get('deposit')
        day_journal.cash_withdrawal = params.get('rows')[0].get('withdrawal')
        [transaction.delete() for transaction in day_journal.cash_deposit_transactions.all()]
        day_journal.cash_deposit_transactions.add(
            dr(bank_account, params.get('rows')[0].get('deposit'), day_journal.date),
            cr(cash_account, params.get('rows')[0].get('deposit'), day_journal.date),
        )
        [transaction.delete() for transaction in day_journal.cash_withdrawal_transactions.all()]
        day_journal.cash_withdrawal_transactions.add(
            cr(bank_account, params.get('rows')[0].get('withdrawal'), day_journal.date),
            dr(cash_account, params.get('rows')[0].get('withdrawal'), day_journal.date),
        )
        dct['saved'][0] = 0
    invalid_attrs = invalid(params.get('rows')[1], ['deposit'])
    if invalid_attrs:
        dct['invalid_attributes'][1] = invalid_attrs
    else:
        day_journal.cheque_deposit = params.get('rows')[1].get('deposit')
        [transaction.delete() for transaction in day_journal.cheque_deposit_transactions.all()]
        day_journal.cheque_deposit_transactions.add(
            dr(bank_account, params.get('rows')[1].get('deposit'), day_journal.date),
            cr(cheque_account, params.get('rows')[0].get('deposit'), day_journal.date),
        )
        dct['saved'][1] = 1
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")