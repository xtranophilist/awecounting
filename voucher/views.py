import json
from datetime import date
from django.core.urlresolvers import reverse, reverse_lazy

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from forms import InvoiceForm, PurchaseVoucherForm, CashReceiptForm
from users.models import group_required
from voucher.models import Invoice, PurchaseVoucher, InvoiceParticular, PurchaseParticular, JournalVoucher, \
    JournalVoucherRow, CashReceipt, CashReceiptRow, CashPayment, CashPaymentRow, FixedAsset, FixedAssetRow, AdditionalDetail
from voucher.serializers import InvoiceSerializer, PurchaseVoucherSerializer, JournalVoucherSerializer, CashReceiptSerializer, CashPaymentSerializer, FixedAssetSerializer
from acubor.lib import invalid, save_model, all_empty_in_dict
from ledger.models import delete_rows, Account, set_transactions, Party, Category
from voucher.filters import InvoiceFilter, PurchaseVoucherFilter
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
def invoice(request, id=None):
    from core.models import VoucherSetting
    from core.models import CompanySetting

    try:
        voucher_setting = VoucherSetting.objects.get(company=request.company)
        company_setting = CompanySetting.objects.get(company=request.company)
    except CompanySetting.DoesNotExist:
        #TODO Add a flash message
        return redirect('/settings/company')
    if id:
        invoice = get_object_or_404(Invoice, id=id, company=request.company)
        scenario = 'Update'
    else:
        invoice = Invoice(date=date.today(),
                          currency=company_setting.default_currency,
                          company= request.company
        )
        scenario = 'Create'
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
                      'description': params.get('description'),
                      'reference': params.get('reference'), 'date': params.get('date'),
                      'due_date': params.get('due_date'), 'tax': params.get('tax'),
                      'currency_id': params.get('currency'), 'company': request.company, 'status': 'Unapproved',
                      'pending_amount': params.get('total_amount'), 'total_amount': params.get('total_amount')}
    # try:
    if params.get('id'):
        invoice = Invoice.objects.get(id=params.get('id'))
    else:
        invoice = Invoice()
        # if not created:
    if invoice_values['total_amount'] == '':
        invoice_values['total_amount'] = 0
    if invoice_values['pending_amount'] == '':
        invoice_values['pending_amount'] = 0
    invoice = save_model(invoice, invoice_values)
    dct['id'] = invoice.id
    # except Exception as e:
    #
    #     if hasattr(e, 'messages'):
    #         dct['error_message'] = '; '.join(e.messages)
    #     else:
    #         dct['error_message'] = 'Error in form data!'
    model = InvoiceParticular
    for index, row in enumerate(params.get('particulars').get('rows')):
        if invalid(row, ['item_id', 'unit_price', 'quantity']):
            continue
        if row.get('discount') == '':
            row['discount'] = 0
        values = {'sn': index + 1, 'item_id': row.get('item_id'), 'description': row.get('description'),
                  'unit_price': row.get('unit_price'), 'quantity': row.get('quantity'), 'discount': row.get('discount'),
                  'tax_scheme_id': row.get('tax_scheme'), 'invoice': invoice}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('particulars').get('deleted_rows'), model)
    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('new_invoice'))}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Owner', 'SuperOwner', 'Supervisor')
def approve_invoice(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        voucher = Invoice.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
        #cash_account = Account.objects.get(name='Cash Account', company=request.company)
    sales_tax_account = Account.objects.get(name='Sales Tax', company=request.company)
    for row in voucher.particulars.all():
        #print row
        ##sales-cr;tax-cr;cash-dr
        #TODO reduce db query by sending tax rate from client
        tax_percent = row.tax_scheme.percent
        wo_discount = row.quantity * row.unit_price
        amt = wo_discount - ((row.discount * wo_discount) / 100)
        if voucher.tax == 'inclusive':
            tax_amount = amt * (tax_percent / (100 + tax_percent))
            net_amount = amt
        elif voucher.tax == 'exclusive':
            tax_amount = amt * (tax_percent / 100)
            net_amount = amt - tax_amount
        elif voucher.tax == 'no':
            tax_amount = 0
            net_amount = amt
        sales_account = row.item.sales_account
        set_transactions(row, voucher.date,
                         ['dr', voucher.party.customer_account, amt],
                         ['cr', sales_account, net_amount],
                         ['cr', sales_tax_account, tax_amount],
        )
    voucher.status = 'Approved'
    voucher.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def cancel_invoice(request):
    r = save_invoice(request)
    dct = json.loads(r.content)
    obj = Invoice.objects.get(id=dct.get('id'))
    obj.status = 'Cancelled'
    obj.save()
    return r


@group_required('Owner', 'SuperOwner', 'Supervisor')
def approve_purchase(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        voucher = PurchaseVoucher.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    for row in voucher.particulars.all():
        wo_discount = row.quantity * row.unit_price
        amt = wo_discount - ((row.discount * wo_discount) / 100)
        set_transactions(row, voucher.date,
                         ['dr', voucher.party.supplier_account, amt],
                         ['cr', row.item.purchase_account, amt],
        )
    voucher.status = 'Approved'
    voucher.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


#@login_required
#def cancel_purchase(request):
#    params = json.loads(request.body)
#    if params.get('id'):
#        id = params.get('id')
#    else:
#        id = None
#    r = purchase_voucher(request, id)
#    import pdb
#    pdb.set_trace()
#    dct = json.loads(r.content)
#    obj = PurchaseVoucher.objects.get(id=dct.get('id'))
#    obj.status = 'Cancelled'
#    obj.save()
#    return r


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
        voucher = PurchaseVoucher(date=date.today(), currency=company_setting.default_currency, tax='no',
                                  company=request.company)
        scenario = 'Create'
    if request.POST.get('action') == 'Cancel':
        voucher.voucher_no = request.POST.get('voucher_no')
        voucher.status = 'Cancelled'
        voucher.save()
        return redirect(reverse_lazy('view_purchase_voucher', kwargs={'id': voucher.id}))
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
            if voucher.total_amount == '':
                voucher.total_amount = 0
            if voucher.pending_amount == '':
                voucher.pending_amount = 0
            voucher.status = 'Unapproved'
            voucher.save()
            model = PurchaseParticular

            for index, row in enumerate(particulars.get('rows')):
                if invalid(row, ['item_id', 'unit_price', 'quantity']):
                    continue
                values = {'sn': index + 1, 'item_id': row.get('item_id'), 'description': row.get('description'),
                          'unit_price': row.get('unit_price'), 'quantity': row.get('quantity'),
                          'discount': row.get('discount'), 'purchase_voucher': voucher}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
            delete_rows(particulars.get('deleted_rows'), model)
            if request.POST.get('action') == 'Save and Continue':
                return redirect(reverse_lazy('new_purchase_voucher'))
            return redirect(reverse_lazy('view_purchase_voucher', kwargs={'id': voucher.id}))
    else:
        form = PurchaseVoucherForm(instance=voucher, company=request.company)
    purchase_voucher_data = PurchaseVoucherSerializer(voucher).data
    return render(request, 'purchase_voucher.html', {'form': form, 'data': purchase_voucher_data, 'scenario': scenario})


@login_required
def journal_voucher(request, id=None):
    if id:
        voucher = get_object_or_404(JournalVoucher, id=id, company=request.company)
        scenario = 'Update'
    else:
        voucher = JournalVoucher(company=request.company, date=date.today())
        scenario = 'Create'
    data = JournalVoucherSerializer(voucher).data
    return render(request, 'journal_voucher.html', {'data': data, 'scenario': scenario})


@login_required
def cancel_journal_voucher(request):
    r = save_journal_voucher(request)
    dct = json.loads(r.content)
    obj = JournalVoucher.objects.get(id=dct.get('id'))
    obj.status = 'Cancelled'
    obj.save()
    return r


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
    if params.get('id'):
        voucher = JournalVoucher.objects.get(id=params.get('id'))
    else:
        voucher = JournalVoucher(company=request.company)
    try:
        existing = JournalVoucher.objects.get(voucher_no=params.get('voucher_no'), company=request.company)
        if voucher.id is not existing.id:
            return HttpResponse(json.dumps({'error_message': 'Voucher no. already exists'}),
                                mimetype="application/json")
    except JournalVoucher.DoesNotExist:
        pass
    voucher_values = {'date': params.get('date'), 'voucher_no': params.get('voucher_no'), 'status': 'Unapproved',
                      'narration': params.get('narration'), 'company': request.company}
    voucher = save_model(voucher, voucher_values)
    dct['id'] = voucher.id
    model = JournalVoucherRow
    for index, row in enumerate(params.get('journal_voucher').get('rows')):
        if invalid(row, ['account']):
            continue
        empty_to_None(row, ['dr_amount', 'cr_amount'])
        values = {'account_id': row.get('account'), 'dr_amount': row.get('dr_amount'),
                  'cr_amount': row.get('cr_amount'), 'type': row.get('type'),
                  'journal_voucher': voucher}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)

        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('journal_voucher').get('deleted_rows'), model)
    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('new_journal_voucher'))}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Owner', 'SuperOwner', 'Supervisor')
def approve_journal_voucher(request):
    params = json.loads(request.body)
    dct = {'rows': []}
    if params.get('id'):
        voucher = JournalVoucher.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    for row in voucher.rows.all():
        if row.type == 'Dr':
            set_transactions(row, voucher.date,
                             ['dr', row.account, row.dr_amount],
            )
        else:
            set_transactions(row, voucher.date,
                             ['cr', row.account, row.cr_amount],
            )
        dct['rows'].append(row.id)
    voucher.status = 'Approved'
    voucher.save()
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
    obj = get_object_or_404(JournalVoucher, id=id, company=request.company)
    obj.delete()
    return redirect(reverse('list_journal_vouchers'))


@login_required
def list_cash_receipts(request):
    pass


@login_required
def cash_receipt(request, id=None):
    if id:
        voucher = get_object_or_404(CashReceipt, id=id, company=request.company)
        scenario = 'Update'
    else:
        voucher = CashReceipt(company=request.company, receipt_on=date.today())
        scenario = 'Create'
    form = CashReceiptForm(instance=voucher, company=request.company)
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

    # try:
    if params.get('id'):
        voucher = CashReceipt.objects.get(id=params.get('id'), company=request.company)
    else:
        voucher = CashReceipt(company=request.company)
        # if not created:
    try:
        existing = CashReceipt.objects.get(voucher_no=params.get('voucher_no'), company=request.company)
        if voucher.id is not existing.id:
            return HttpResponse(json.dumps({'error_message': 'Voucher no. already exists'}),
                                mimetype="application/json")
    except CashReceipt.DoesNotExist:
        pass
    values = {'party_id': params.get('party'), 'receipt_on': params.get('receipt_on'),
              'voucher_no': params.get('voucher_no'),
              'reference': params.get('reference'), 'company': request.company}
    voucher = save_model(voucher, values)
    dct['id'] = voucher.id
    # except Exception as e:
    #
    #     if hasattr(e, 'messages'):
    #         dct['error_message'] = '; '.join(e.messages)
    #     else:
    #         dct['error_message'] = 'Error in form data!'
    model = CashReceiptRow
    if params.get('table_vm').get('rows'):
        for index, row in enumerate(params.get('table_vm').get('rows')):
            if invalid(row, ['payment']) and invalid(row, ['discount']):
                continue
            if (row.get('discount') == '') | (row.get('discount') is None):
                row['discount'] = 0
            if (row.get('payment') == '') | (row.get('payment') is None):
                row['payment'] = 0
            invoice = Invoice.objects.get(invoice_no=row.get('bill_no'), company=request.company)
            values = {'discount': row.get('discount'), 'receipt': row.get('payment'),
                      'cash_receipt': voucher,
                      'invoice': invoice}
            submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
            if not created:
                submodel = save_model(submodel, values)
            dct['rows'][index] = submodel.id
        total = float(params.get('total_payment')) + float(params.get('total_discount'))
        voucher.amount = total
        voucher.status = 'Unapproved'
        voucher.save()
    else:
        voucher.amount = params.get('amount')
        voucher.status = 'Unapproved'
        voucher.save()
    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('create_cash_receipt'))}
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
        voucher = CashPayment(company=request.company, payment_on=date.today())
        scenario = 'Create'
    data = CashPaymentSerializer(voucher).data
    return render(request, 'cash_payment.html', {'scenario': scenario, 'data': data})


@login_required
def party_purchase_vouchers(request, id):
    objs = PurchaseVoucher.objects.filter(company=request.company, party=Party.objects.get(id=id), pending_amount__gt=0)
    lst = []
    for obj in objs:
        lst.append({'id': obj.id, 'bill_no': obj.reference, 'date': obj.date, 'total_amount': obj.total_amount,
                    'pending_amount': obj.pending_amount, 'due_date': obj.due_date})
    return HttpResponse(json.dumps(lst, default=handler), mimetype="application/json")


@login_required
def save_cash_payment(request):
    params = json.loads(request.body)
    dct = {'rows': {}}

    # try:
    if params.get('id'):
        voucher = CashPayment.objects.get(id=params.get('id'))
    else:
        voucher = CashPayment(company=request.company)
    try:
        existing = CashPayment.objects.get(voucher_no=params.get('voucher_no'), company=request.company)
        if voucher.id is not existing.id:
            return HttpResponse(json.dumps({'error_message': 'Voucher no. already exists'}),
                                mimetype="application/json")
    except CashPayment.DoesNotExist:
        pass
    values = {'party_id': params.get('party'), 'payment_on': params.get('payment_on'),
              'voucher_no': params.get('voucher_no'),
              'reference': params.get('reference'), 'company': request.company}
    voucher = save_model(voucher, values)
    dct['id'] = voucher.id
    # except Exception as e:
    #
    #     if hasattr(e, 'messages'):
    #         dct['error_message'] = '; '.join(e.messages)
    #     else:
    #         dct['error_message'] = 'Error in form data!'
    model = CashPaymentRow
    if params.get('table_vm').get('rows'):
        for index, row in enumerate(params.get('table_vm').get('rows')):
            print row
            if invalid(row, ['payment']) and invalid(row, ['discount']):
                continue
            if (row.get('discount') == '') | (row.get('discount') is None):
                row['discount'] = 0
            if (row.get('payment') == '') | (row.get('payment') is None):
                row['payment'] = 0
            purchase_voucher = PurchaseVoucher.objects.get(id=row.get('id'), company=request.company)
            values = {'discount': row.get('discount'), 'payment': row.get('payment'),
                      'cash_payment': voucher,
                      'purchase_voucher': purchase_voucher}
            submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
            if not created:
                submodel = save_model(submodel, values)
            dct['rows'][index] = submodel.id
        total = float(params.get('total_payment')) + float(params.get('total_discount'))
        voucher.amount = total
        voucher.status = 'Unapproved'
        voucher.save()
    else:
        voucher.amount = params.get('amount')
        voucher.status = 'Unapproved'
        voucher.save()
    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('create_cash_payment'))}
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
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
    discount_expenses_account = Account.objects.get(name='Discount Expenses', company=request.company)
    if voucher.rows.all().count() > 0:
        total_receipt = sum(row.receipt for row in voucher.rows.all())
        total_discount = sum(row.discount for row in voucher.rows.all())
        total = total_receipt + total_discount
        set_transactions(voucher, voucher.receipt_on,
                         ['dr', cash_account, total_receipt],
                         ['dr', discount_expenses_account, total_discount],
                         ['cr', voucher.party.customer_account, total]
        )
    else:
        set_transactions(voucher, voucher.receipt_on,
                         ['dr', cash_account, voucher.amount],
                         ['cr', voucher.party.customer_account, voucher.amount]
        )
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('SuperOwner', 'Owner', 'Supervisor')
def approve_cash_payment(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        voucher = CashPayment.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    cash_account = Account.objects.get(name='Cash Account', company=request.company)
    discount_income_account = Account.objects.get(name='Discount Income', company=request.company)
    if voucher.rows.all().count() > 0:
        total_payment = sum(row.payment for row in voucher.rows.all())
        total_discount = sum(row.discount for row in voucher.rows.all())
        total = total_payment + total_discount
        set_transactions(voucher, voucher.payment_on,
                         ['dr', voucher.party.supplier_account, total],
                         ['cr', discount_income_account, total_discount],
                         ['cr', cash_account, total_payment]
        )
    else:
        set_transactions(voucher, voucher.payment_on,
                         ['dr', cash_account, voucher.amount],
                         ['cr', voucher.party.supplier_account, voucher.amount]
        )
    voucher.status = 'Approved'
    voucher.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def list_fixed_assets(request):
    objs = FixedAsset.objects.filter(company=request.company)
    #filtered_items = InvoiceFilter(request.GET, queryset=objs, company=request.company)
    return render(request, 'list_fixed_assets.html', {'objects': objs})


@login_required
def fixed_asset(request, id=None):
    if id:
        voucher = get_object_or_404(FixedAsset, id=id, company=request.company)
        scenario = 'Update'
    else:
        voucher = FixedAsset(date=date.today(), company=request.company)
        scenario = 'Create'
    data = FixedAssetSerializer(voucher).data
    fixed_asset_category = Category.objects.get(name='Fixed Assets', company=request.company)
    return render(request, 'fixed_asset.html',
                  {'scenario': scenario, 'data': data, 'fixed_asset_category': fixed_asset_category})


@login_required
def save_fixed_asset(request):
    params = json.loads(request.body)
    dct = {'rows1': {}, 'rows2': {}}
    if params.get('id'):
        voucher = FixedAsset.objects.get(id=params.get('id'))
    else:
        voucher = FixedAsset(company=request.company)
    try:
        existing = FixedAsset.objects.get(voucher_no=params.get('voucher_no'), company=request.company)
        if voucher.id is not existing.id:
            return HttpResponse(json.dumps({'error_message': 'Voucher no. already exists'}),
                                mimetype="application/json")
    except FixedAsset.DoesNotExist:
        pass
    voucher_values = {'date': params.get('date'), 'voucher_no': params.get('voucher_no'),
                      'description': params.get('description'), 'company': request.company, 'status': 'Unapproved',
                      'from_account_id': params.get('from_account'), 'reference': params.get('reference')}
    voucher = save_model(voucher, voucher_values)
    dct['id'] = voucher.id
    model = FixedAssetRow
    for index, row in enumerate(params.get('table_vm').get('rows')):
        if invalid(row, ['asset_ledger', 'amount']):
            continue
        values = {'asset_ledger_id': row.get('asset_ledger'), 'description': row.get('description'),
                  'amount': row.get('amount'), 'fixed_asset': voucher}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows1'][index] = submodel.id
    delete_rows(params.get('table_vm').get('deleted_rows'), model)
    model = AdditionalDetail
    for index, row in enumerate(params.get('additional_details').get('rows')):
        values = {'assets_code': row.get('assets_code'), 'assets_type': row.get('assets_type'),
                  'vendor_name': row.get('vendor_name'), 'vendor_address': row.get('vendor_address'),
                  'amount': row.get('amount'), 'useful_life': row.get('useful_life'),
                  'description': row.get('description'), 'warranty_period': row.get('warranty_period'),
                  'maintenance': row.get('maintenance')}
        if all_empty_in_dict(values):
            continue
        values['fixed_asset'] = voucher
        if row.get('amount') == '':
            values['amount'] = None
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows2'][index] = submodel.id
    delete_rows(params.get('additional_details').get('deleted_rows'), model)
    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('create_fixed_asset'))}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def approve_fixed_asset(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        voucher = FixedAsset.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    for row in voucher.rows.all():
        set_transactions(row, voucher.date,
                         ['dr', row.asset_ledger, row.amount],
                         ['cr', voucher.from_account, row.amount])
    voucher.status = 'Approved'
    voucher.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")