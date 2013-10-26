import json
from datetime import date
from django.core.urlresolvers import reverse, reverse_lazy

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from forms import InvoiceForm, PurchaseVoucherForm, CashReceiptForm
from users.models import group_required
from voucher.models import Invoice, PurchaseVoucher, InvoiceParticular, PurchaseParticular, JournalVoucher, \
    JournalVoucherRow, CashReceipt, CashReceiptRow, CashPayment, CashPaymentRow
from voucher.serializers import InvoiceSerializer, PurchaseVoucherSerializer, \
    JournalVoucherSerializer, CashReceiptSerializer, CashPaymentSerializer
from acubor.lib import invalid, save_model
from ledger.models import delete_rows, Account, set_transactions, Party
from voucher.filters import InvoiceFilter, PurchaseVoucherFilter
from tax.models import TaxScheme
from inventory.models import Item
from voucher.templatetags.filters import handler


@login_required
def all_invoices(request):
    items = Invoice.objects.filter(company=request.company)
    filtered_items = InvoiceFilter(request.GET, queryset=items, company=request.company)
    return render(request, 'list_invoice.html', {'objects': filtered_items})


@login_required
def all_purchase_vouchers(request):
    items = PurchaseVoucher.objects.filter(company=request.company)
    filtered_items = PurchaseVoucherFilter(request.GET, queryset=items, company=request.company)
    return render(request, 'all_purchase_vouchers.html', {'objects': filtered_items})


@login_required
def invoice(request, invoice_no=None):
    from core.models import VoucherSetting
    from core.models import CompanySetting

    try:
        voucher_setting = VoucherSetting.objects.get(company=request.company)
        company_setting = CompanySetting.objects.get(company=request.company)
    except CompanySetting.DoesNotExist:
        #TODO Add a flash message
        return redirect('/settings/company')
    if invoice_no:
        invoice = get_object_or_404(Invoice, invoice_no=invoice_no, company=request.company)
        scenario = 'Update'
    else:
        invoice = Invoice(date=date.today(),
                          currency=company_setting.default_currency
        )
        scenario = 'Create'
        try:
            try:
                last_invoice = Invoice.objects.filter(company=request.company).latest('id')
                last_invoice_no = last_invoice.invoice_no
            except Invoice.DoesNotExist:
                # for first invoice
                last_invoice_no = 0
            new_invoice_no = int(last_invoice_no) + 1
            invoice.invoice_no = "0" * (int(voucher_setting.invoice_digit_count) - str(new_invoice_no).__len__()) \
                                 + str(new_invoice_no)
        except:
            invoice.invoice_no = ''

    form = InvoiceForm(data=request.POST, instance=invoice, company=request.company)
    invoice_data = InvoiceSerializer(invoice).data
    invoice_data['read_only'] = {
        'invoice_heading': voucher_setting.invoice_heading,
        'invoice_prefix': voucher_setting.invoice_prefix,
        'invoice_suffix': voucher_setting.invoice_suffix,
    }
    return render(request, 'invoice.html', {'form': form, 'data': invoice_data, 'scenario': scenario})


@login_required
def save_invoice(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    invoice_values = {'party_id': params.get('party'), 'invoice_no': params.get('invoice_no'),
                      'reference': params.get('reference'), 'date': params.get('date'),
                      'due_date': params.get('due_date'), 'tax': params.get('tax'),
                      'currency_id': params.get('currency'), 'company': request.company,
                      'pending_amount': params.get('total_amount'), 'total_amount': params.get('total_amount')}
    # try:
    if params.get('id'):
        invoice = Invoice.objects.get(id=params.get('id'))
    else:
        invoice = Invoice()
        # if not created:
    invoice = save_model(invoice, invoice_values)
    dct['id'] = invoice.id
    # except Exception as e:
    #
    #     if hasattr(e, 'messages'):
    #         dct['error_message'] = '; '.join(e.messages)
    #     else:
    #         dct['error_message'] = 'Error in form data!'
    model = InvoiceParticular
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
    sales_tax_account = Account.objects.get(name='Sales Tax', company=request.company)
    print params
    for index, row in enumerate(params.get('particulars').get('rows')):
        if invalid(row, ['item_id', 'unit_price', 'quantity']):
            continue
        if row.get('discount') == '':
            row['discount'] = 0
        values = {'sn': index + 1, 'item_id': row.get('item_id'), 'description': row.get('description'),
                  'unit_price': row.get('unit_price'), 'quantity': row.get('quantity'), 'discount': row.get('discount'),
                  'tax_scheme_id': row.get('tax_scheme'), 'invoice': invoice}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        #sales-cr;tax-cr;cash-dr
        #TODO reduce db query by sending tax rate from client
        tax_percent = TaxScheme.objects.get(id=row.get('tax_scheme')).percent
        wo_discount = float(row.get('quantity')) * float(row.get('unit_price'))
        amt = wo_discount - ((float(row.get('discount')) * wo_discount) / 100)
        if params.get('tax') == 'inclusive':
            tax_amount = amt * (tax_percent / (100 + tax_percent))
            net_amount = amt
        elif params.get('tax') == 'exclusive':
            tax_amount = amt * (tax_percent / 100)
            net_amount = amt - tax_amount
        elif params.get('tax') == 'no':
            tax_amount = 0
            net_amount = amt
        sales_account = Item.objects.get(id=row.get('item_id')).sales_account
        set_transactions(submodel, params.get('date'),
                         ['dr', cash_account, amt],
                         ['cr', sales_account, net_amount],
                         ['cr', sales_tax_account, tax_amount],
        )
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('particulars').get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_invoice_and_continue(request):
    pass


@group_required('Owner', 'SuperOwner', 'Supervisor')
def approve_invoice(request):
    pass


@login_required
def cancel_invoice(request):
    pass


@login_required
def delete_invoice(request, invoice_no):
    obj = Invoice.objects.get(invoice_no=invoice_no, company=request.company)
    obj.delete()
    return redirect(reverse('all_invoices'))
    #return redirect('/voucher/invoices/')


@login_required
def delete_purchase_voucher(request, id):
    obj = PurchaseVoucher.objects.get(id=id, company=request.company)
    obj.delete()
    return redirect(reverse('all_purchase_vouchers'))


@login_required
def purchase_voucher(request, id=None):
    from core.models import CompanySetting

    try:
        company_setting = CompanySetting.objects.get(company=request.company)
    except CompanySetting.DoesNotExist:
        return redirect('/settings/company')
    if id:
        voucher = get_object_or_404(PurchaseVoucher, id=id, company=request.company)
        scenario = 'Update'
    else:
        voucher = PurchaseVoucher(date=date.today(), currency=company_setting.default_currency, tax='no')
        scenario = 'Create'
    if request.POST:
        form = PurchaseVoucherForm(request.POST, request.FILES, instance=voucher, company=request.company)
        if form.is_valid():
            particulars = json.loads(request.POST['particulars'])
            voucher = form.save(commit=False)
            if 'attachment' in request.FILES:
                voucher.attachment = request.FILES['attachment']
            voucher.total_amount = particulars.get('grand_total')
            voucher.pending_amount = particulars.get('grand_total')
            voucher.company = request.company
            voucher.save()

        if id or form.is_valid():
            model = PurchaseParticular
            cash_account = Account.objects.get(name='Cash Account', company=request.company)
            for index, row in enumerate(particulars.get('rows')):
                if invalid(row, ['item_id', 'unit_price', 'quantity']):
                    continue
                values = {'sn': index + 1, 'item_id': row.get('item_id'), 'description': row.get('description'),
                          'unit_price': row.get('unit_price'), 'quantity': row.get('quantity'),
                          'discount': row.get('discount'), 'purchase_voucher': voucher}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                wo_discount = float(row.get('quantity')) * float(row.get('unit_price'))
                amt = wo_discount - ((float(row.get('discount')) * wo_discount) / 100)
                purchase_account = Item.objects.get(id=row.get('item_id')).purchase_account
                set_transactions(submodel, request.POST['date'],
                                 ['dr', cash_account, amt],
                                 ['cr', purchase_account, amt],
                )
                if not created:
                    submodel = save_model(submodel, values)
            delete_rows(particulars.get('deleted_rows'), model)
            return redirect('/voucher/purchases/')
    form = PurchaseVoucherForm(instance=voucher, company=request.company)
    purchase_voucher_data = PurchaseVoucherSerializer(voucher).data
    return render(request, 'purchase_voucher.html', {'form': form, 'data': purchase_voucher_data, 'scenario': scenario})


@login_required
def journal_voucher(request, id=None):
    if id:
        voucher = get_object_or_404(JournalVoucher, id=id, company=request.company)
        scenario = 'Update'
    else:
        voucher = JournalVoucher()
        scenario = 'Create'
    data = JournalVoucherSerializer(voucher).data
    return render(request, 'journal_voucher.html', {'data': data, 'scenario': scenario})


def empty_to_None(dict, list_of_attr):
    for attr in list_of_attr:
        if dict.get(attr) == '':
            dict[attr] = None
    return dict


@login_required
def list_journal_vouchers(request):
    objects = JournalVoucher.objects.filter(company=request.company)
    return render(request, 'list_journal_vouchers.html', {'objects': objects})


@login_required
def save_journal_voucher(request):
    params = json.loads(request.body)
    dct = {'rows': {}}

    voucher_values = {'date': params.get('date'), 'voucher_no': params.get('voucher_no'),
                      'narration': params.get('narration'), 'company': request.company}
    if params.get('id'):
        voucher = JournalVoucher.objects.get(id=params.get('id'))
    else:
        voucher = JournalVoucher()
    voucher = save_model(voucher, voucher_values)
    dct['id'] = voucher.id
    model = JournalVoucherRow
    for index, row in enumerate(params.get('journal_voucher').get('rows')):
        empty_to_None(row, ['dr_amount', 'cr_amount'])
        values = {'account_id': row.get('account'), 'dr_amount': row.get('dr_amount'),
                  'cr_amount': row.get('cr_amount'), 'type': row.get('type'),
                  'journal_voucher': voucher}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if row.get('type') == 'Dr':
            print 'dr'
            set_transactions(submodel, params.get('date'),
                             ['dr', Account.objects.get(id=row.get('account')), row.get('dr_amount')],
            )
        else:
            set_transactions(submodel, params.get('date'),
                             ['cr', Account.objects.get(id=row.get('account')), row.get('cr_amount')],
            )
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('journal_voucher').get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")

#
# def bank_voucher(request, id=None):
#     if id:
#         voucher = get_object_or_404(JournalVoucher, id=id)
#     else:
#         voucher = JournalVoucher()
#     data = JournalVoucherSerializer(voucher).data
#     return render(request, 'bank_voucher.html', {'data': data})
#
#
# def save_bank_voucher(request):
#     params = json.loads(request.body)
#     dct = {'rows': {}}
#
#     del [params['accounts']]
#     del [params['journal_voucher']['_initial_rows']]
#
#     voucher_values = {'date': params.get('date'), 'company': request.company}
#     if params.get('id'):
#         voucher = JournalVoucher.objects.get(id=params.get('id'))
#     else:
#         voucher = JournalVoucher()
#     voucher = save_model(voucher, voucher_values)
#     dct['id'] = voucher.id
#     model = JournalVoucherRow
#     for index, row in enumerate(params.get('journal_voucher').get('rows')):
#         # print row.get('dr_account_id')
#         empty_to_None(row, ['dr_amount'], 'cr_amount')
#         values = {'sn': index + 1, 'dr_account_id': row.get('dr_account_id'), 'dr_amount': row.get('dr_amount'),
#                   'cr_account_id': row.get('cr_account_id'), 'cr_amount': row.get('cr_amount'),
#                   'journal_voucher': voucher}
#         from django.db import transaction, IntegrityError
#
#         submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
#         if not created:
#             submodel = save_model(submodel, values)
#         dct['rows'][index] = submodel.id
#     delete_rows(params.get('journal_voucher').get('deleted_rows'), model)
#     return HttpResponse(json.dumps(dct), mimetype="application/json")
#
#
# def save_bank_detail(request, account_id):
#     # bank_account = Account.objects.get(id=account_id)
#     # params = json.loads(request.body)
#     # day_journal = get_journal(request)
#     # bank_detail, created = BankDetail.objects.get_or_create(day_journal=day_journal, bank_account=bank_account)
#     dct = {'invalid_attributes': {}, 'saved': {}}
#     # model = BankDetailRow
#     # print params
#     # for index, row in enumerate(params.get('rows')):
#     #     invalid_attrs = invalid(row, ['type', 'account_id', 'amount'])
#     #     if invalid_attrs:
#     #         dct['invalid_attributes'][index] = invalid_attrs
#     #         continue
#     #     values = {'sn': index+1, 'type': row.get('type'), 'amount': row.get('amount'),
#     #               'account_id': row.get('account_id'), 'bank_detail': bank_detail}
#     #     submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
#     #     if not created:
#     #         submodel = save_model(submodel, values)
#     #     dct['saved'][index] = submodel.id
#     # delete_rows(params.get('deleted_rows'), model)
#     return HttpResponse(json.dumps(dct), mimetype="application/json")

@login_required
def delete_journal_voucher(request, id):
    obj = JournalVoucher.objects.get(id=id, company=request.company)
    obj.delete()
    return redirect(reverse('all_journal_vouchers'))


@login_required
def list_cash_receipts(request):
    pass


@login_required
def cash_receipt(request, id=None):
    if id:
        voucher = get_object_or_404(CashReceipt, id=id, company=request.company)
        scenario = 'Update'
    else:
        voucher = CashReceipt()
        scenario = 'Create'
    form = CashReceiptForm(instance=voucher)
    data = CashReceiptSerializer(voucher).data
    return render(request, 'cash_receipt.html', {'form': form, 'scenario': scenario, 'data': data})


@login_required
def party_invoices(request, id):
    objs = Invoice.objects.filter(company=request.company, party=Party.objects.get(id=id), pending_amount__gt=0)
    lst = []
    for obj in objs:
        lst.append({'id': obj.id, 'bill_no': obj.invoice_no, 'date': obj.date, 'total_amount': obj.total_amount,
                    'pending_amount': obj.pending_amount, 'due_date': obj.due_date})
    return HttpResponse(json.dumps(lst, default=handler), mimetype="application/json")


@login_required
def save_cash_receipt(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    values = {'party_id': params.get('party'), 'receipt_on': params.get('receipt_on'),
              'reference': params.get('reference'), 'company': request.company}
    # try:
    if params.get('id'):
        voucher = CashReceipt.objects.get(id=params.get('id'))
    else:
        voucher = CashReceipt()
        # if not created:
    voucher = save_model(voucher, values)
    dct['id'] = voucher.id
    # except Exception as e:
    #
    #     if hasattr(e, 'messages'):
    #         dct['error_message'] = '; '.join(e.messages)
    #     else:
    #         dct['error_message'] = 'Error in form data!'
    model = CashReceiptRow
    #cash_account = Account.objects.get(name='Cash Account', company=request.company)
    #sales_tax_account = Account.objects.get(name='Sales Tax', company=request.company)
    if params.get('table_vm').get('rows'):
        for index, row in enumerate(params.get('table_vm').get('rows')):
            if invalid(row, ['payment']) and invalid(row, ['discount']):
                continue
            if (row.get('discount') == '') | (row.get('discount') is None):
                row['discount'] = 0
            if (row.get('payment') == '') | (row.get('payment') is None):
                row['payment'] = 0
            print row
            values = {'discount': row.get('discount'), 'receipt': row.get('payment'),
                      'cash_receipt': voucher,
                      'invoice': Invoice.objects.get(invoice_no=row.get('bill_no'), company=request.company)}
            submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
            if not created:
                submodel = save_model(submodel, values)
            dct['rows'][index] = submodel.id
        total = float(params.get('total_payment')) + float(params.get('total_discount'))
        voucher.amount = total
        voucher.save()
    else:
        voucher.amount = params.get('amount')
        voucher.save()
    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('create_cash_receipt'))}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('SuperOwner', 'Owner', "supervisor")
def approve_cash_receipt(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        voucher = CashReceipt.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
        #set_transactions(voucher, params.get('receipt_on'),
    #                         ['cr', Account.objects.get(id=params.get('total_payment')), row.get('cr_amount')],
    #        )
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
    discount_expenses_account = Account.objects.get(name='Discounting Expenses', company=request.company)
    if params.get('table_vm') and params.get('table_vm').get('rows'):
        total = float(params.get('total_payment')) + float(params.get('total_discount'))
        set_transactions(voucher, params.get('receipt_on'),
                         ['dr', cash_account, params.get('total_payment')],
                         ['dr', discount_expenses_account, params.get('total_payment')],
                         ['cr', Party.objects.get(id=params.get('party')).customer_account, total]
        )
    else:
        set_transactions(voucher, params.get('receipt_on'),
                         ['dr', cash_account, params.get('amount')],
                         #['dr', discount_expenses_account, params.get('total_payment')],
                         ['cr', Party.objects.get(id=params.get('party')).customer_account, params.get('amount')]
        )
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def list_cash_payments(request):
    pass


@login_required
def cash_payment(request, id=None):
    if id:
        voucher = get_object_or_404(CashPayment, id=id, company=request.company)
        scenario = 'Update'
    else:
        voucher = CashPayment()
        scenario = 'Create'
    #form = CashReceiptForm(instance=voucher)
    data = CashPaymentSerializer(voucher).data
    return render(request, 'cash_payment.html', {'scenario': scenario, 'data': data})


@login_required
def party_purchase_vouchers(request, id):
    objs = PurchaseVoucher.objects.filter(company=request.company, party=Party.objects.get(id=id), pending_amount__gt=0)
    lst = []
    for obj in objs:
        lst.append({'id': obj.id, 'bill_no': obj.invoice_no, 'date': obj.date, 'total_amount': obj.total_amount,
                    'pending_amount': obj.pending_amount, 'due_date': obj.due_date})
    return HttpResponse(json.dumps(lst, default=handler), mimetype="application/json")


@login_required
def save_cash_payment(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    values = {'party_id': params.get('party'), 'receipt_on': params.get('receipt_on'),
              'reference': params.get('reference'), 'company': request.company}
    # try:
    if params.get('id'):
        voucher = CashPayment.objects.get(id=params.get('id'))
    else:
        voucher = CashPayment()
        # if not created:
    voucher = save_model(voucher, values)
    dct['id'] = voucher.id
    # except Exception as e:
    #
    #     if hasattr(e, 'messages'):
    #         dct['error_message'] = '; '.join(e.messages)
    #     else:
    #         dct['error_message'] = 'Error in form data!'
    model = CashPaymentRow
    #cash_account = Account.objects.get(name='Cash Account', company=request.company)
    #sales_tax_account = Account.objects.get(name='Sales Tax', company=request.company)
    if params.get('table_vm').get('rows'):
        for index, row in enumerate(params.get('table_vm').get('rows')):
            if invalid(row, ['payment']) and invalid(row, ['discount']):
                continue
            if (row.get('discount') == '') | (row.get('discount') is None):
                row['discount'] = 0
            if (row.get('payment') == '') | (row.get('payment') is None):
                row['payment'] = 0
            print row
            values = {'discount': row.get('discount'), 'payment': row.get('payment'),
                      'cash_payment': voucher,
                      'purchase_voucher': PurchaseVoucher.objects.get(id=row.get('id'), company=request.company)}
            submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
            if not created:
                submodel = save_model(submodel, values)
            dct['rows'][index] = submodel.id
        total = float(params.get('total_payment')) + float(params.get('total_discount'))
        voucher.amount = total
        voucher.save()
    else:
        voucher.amount = params.get('amount')
        voucher.save()
    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('create_cash_receipt'))}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('SuperOwner', 'Owner', "supervisor")
def approve_cash_payment(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        voucher = CashPayment.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
        #set_transactions(voucher, params.get('receipt_on'),
    #                         ['cr', Account.objects.get(id=params.get('total_payment')), row.get('cr_amount')],
    #        )
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
    discount_expenses_account = Account.objects.get(name='Discounting Expenses', company=request.company)
    if params.get('table_vm') and params.get('table_vm').get('rows'):
        total = float(params.get('total_payment')) + float(params.get('total_discount'))
        set_transactions(voucher, params.get('receipt_on'),
                         ['dr', cash_account, params.get('total_payment')],
                         ['dr', discount_expenses_account, params.get('total_payment')],
                         ['cr', Party.objects.get(id=params.get('party')).customer_account, total]
        )
    else:
        print params.get('amount')

        set_transactions(voucher, params.get('receipt_on'),
                         ['dr', cash_account, params.get('amount')],
                         #['dr', discount_expenses_account, params.get('total_payment')],
                         ['cr', Party.objects.get(id=params.get('party')).customer_account, params.get('amount')]
        )
    return HttpResponse(json.dumps(dct), mimetype="application/json")