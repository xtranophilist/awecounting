import json

from django.shortcuts import render, redirect, get_object_or_404
from datetime import date

from forms import InvoiceForm, PurchaseVoucherForm
from voucher.models import Invoice, PurchaseVoucher, InvoiceParticular, PurchaseParticular, JournalVoucher, \
    JournalVoucherRow
from voucher.serializers import InvoiceSerializer, PurchaseVoucherSerializer, \
    JournalVoucherSerializer
from django.http import HttpResponse
import json
from acubor.lib import invalid, save_model
from ledger.models import delete_rows, Party
from voucher.filters import InvoiceFilter, PurchaseVoucherFilter


def all_invoices(request):
    items = Invoice.objects.filter(company=request.user.company)
    filtered_items = InvoiceFilter(request.GET, queryset=items, company=request.user.company)
    return render(request, 'list_invoice.html', {'objects': filtered_items})


def all_purchase_vouchers(request):
    items = PurchaseVoucher.objects.filter(company=request.user.company)
    filtered_items = PurchaseVoucherFilter(request.GET, queryset=items, company=request.user.company)
    return render(request, 'all_purchase_vouchers.html', {'objects': filtered_items})


def invoice(request, invoice_no=None):
    from core.models import CompanySetting

    try:
        company_setting = CompanySetting.objects.get(company=request.user.company)
    except CompanySetting.DoesNotExist:
        #TODO Add a flash message
        return redirect('/settings/company')
    if invoice_no:
        invoice = get_object_or_404(Invoice, invoice_no=invoice_no)
    else:
        invoice = Invoice(date=date.today(), currency=company_setting.default_currency)
        try:
            try:
                last_invoice = Invoice.objects.latest('id')
                last_invoice_no = last_invoice.invoice_no
            except Invoice.DoesNotExist:
                # for first invoice
                last_invoice_no = 0
            new_invoice_no = int(last_invoice_no) + 1
            invoice.invoice_no = "0" * (int(company_setting.invoice_digit_count) - str(new_invoice_no).__len__()) \
                                 + str(new_invoice_no)
        except:
            invoice.invoice_no = ''

    form = InvoiceForm(data=request.POST, instance=invoice, company=request.user.company)
    invoice_data = InvoiceSerializer(invoice).data
    invoice_data['read_only'] = {
        'invoice_prefix': company_setting.invoice_prefix,
        'invoice_suffix': company_setting.invoice_suffix,
    }
    return render(request, 'invoice.html', {'form': form, 'data': invoice_data})


def save_invoice(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    invoice_values = {'party_id': params.get('party'), 'invoice_no': params.get('invoice_no'),
                      'reference': params.get('reference'), 'date': params.get('date'),
                      'due_date': params.get('due_date'), 'tax': params.get('tax'),
                      'currency_id': params.get('currency'), 'company': request.user.company}
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
    for index, row in enumerate(params.get('particulars').get('rows')):
        if invalid(row, ['item_id', 'unit_price', 'quantity']):
            continue
        values = {'sn': index + 1, 'item_id': row.get('item_id'), 'description': row.get('description'),
                  'unit_price': row.get('unit_price'), 'quantity': row.get('quantity'), 'discount': row.get('discount'),
                  'tax_scheme_id': row.get('tax_scheme'), 'invoice': invoice}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('particulars').get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def purchase_voucher(request, id=None):
    from core.models import CompanySetting

    try:
        company_setting = CompanySetting.objects.get(company=request.user.company)
    except CompanySetting.DoesNotExist:
        return redirect('/settings/company')
    if id:
        voucher = get_object_or_404(PurchaseVoucher, id=id)
    else:
        voucher = PurchaseVoucher(date=date.today(), currency=company_setting.default_currency)

    if request.POST:
        form = PurchaseVoucherForm(request.POST, request.FILES, instance=voucher, company=request.user.company)
        if form.is_valid():
            voucher = form.save(commit=False)
            if 'attachment' in request.FILES:
                voucher.attachment = request.FILES['attachment']
            voucher.company = request.user.company
            voucher.save()
        if id or form.is_valid():
            particulars = json.loads(request.POST['particulars'])
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
    form = PurchaseVoucherForm(instance=voucher, company=request.user.company)
    purchase_voucher_data = PurchaseVoucherSerializer(voucher).data
    return render(request, 'purchase_voucher.html', {'form': form, 'data': purchase_voucher_data})


def journal_voucher(request, id=None):
    if id:
        voucher = get_object_or_404(JournalVoucher, id=id)
    else:
        voucher = JournalVoucher()
    data = JournalVoucherSerializer(voucher).data
    return render(request, 'journal_voucher.html', {'data': data})


def empty_to_None(dict, list_of_attr):
    return dict


def save_journal_voucher(request):
    params = json.loads(request.body)
    dct = {'rows': {}}

    del [params['accounts']]
    del [params['journal_voucher']['_initial_rows']]

    voucher_values = {'date': params.get('date'), 'company': request.user.company}
    if params.get('id'):
        voucher = JournalVoucher.objects.get(id=params.get('id'))
    else:
        voucher = JournalVoucher()
    voucher = save_model(voucher, voucher_values)
    dct['id'] = voucher.id
    model = JournalVoucherRow
    for index, row in enumerate(params.get('journal_voucher').get('rows')):
        # print row.get('dr_account_id')
        empty_to_None(row, ['dr_amount'], 'cr_amount')
        values = {'sn': index + 1, 'dr_account_id': row.get('dr_account_id'), 'dr_amount': row.get('dr_amount'),
                  'cr_account_id': row.get('cr_account_id'), 'cr_amount': row.get('cr_amount'),
                  'journal_voucher': voucher}
        from django.db import transaction, IntegrityError

        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('journal_voucher').get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def bank_voucher(request, id=None):
    if id:
        voucher = get_object_or_404(JournalVoucher, id=id)
    else:
        voucher = JournalVoucher()
    data = JournalVoucherSerializer(voucher).data
    return render(request, 'bank_voucher.html', {'data': data})


def save_bank_voucher(request):
    params = json.loads(request.body)
    dct = {'rows': {}}

    del [params['accounts']]
    del [params['journal_voucher']['_initial_rows']]

    voucher_values = {'date': params.get('date'), 'company': request.user.company}
    if params.get('id'):
        voucher = JournalVoucher.objects.get(id=params.get('id'))
    else:
        voucher = JournalVoucher()
    voucher = save_model(voucher, voucher_values)
    dct['id'] = voucher.id
    model = JournalVoucherRow
    for index, row in enumerate(params.get('journal_voucher').get('rows')):
        # print row.get('dr_account_id')
        empty_to_None(row, ['dr_amount'], 'cr_amount')
        values = {'sn': index + 1, 'dr_account_id': row.get('dr_account_id'), 'dr_amount': row.get('dr_amount'),
                  'cr_account_id': row.get('cr_account_id'), 'cr_amount': row.get('cr_amount'),
                  'journal_voucher': voucher}
        from django.db import transaction, IntegrityError

        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('journal_voucher').get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_bank_detail(request, account_id):
    # bank_account = Account.objects.get(id=account_id)
    # params = json.loads(request.body)
    # day_journal = get_journal(request)
    # bank_detail, created = BankDetail.objects.get_or_create(day_journal=day_journal, bank_account=bank_account)
    dct = {'invalid_attributes': {}, 'saved': {}}
    # model = BankDetailRow
    # print params
    # for index, row in enumerate(params.get('rows')):
    #     invalid_attrs = invalid(row, ['type', 'account_id', 'amount'])
    #     if invalid_attrs:
    #         dct['invalid_attributes'][index] = invalid_attrs
    #         continue
    #     values = {'sn': index+1, 'type': row.get('type'), 'amount': row.get('amount'),
    #               'account_id': row.get('account_id'), 'bank_detail': bank_detail}
    #     submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
    #     if not created:
    #         submodel = save_model(submodel, values)
    #     dct['saved'][index] = submodel.id
    # delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")



