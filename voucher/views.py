import json

from django.shortcuts import render, redirect, get_object_or_404
from datetime import date

from forms import InvoiceForm, PurchaseVoucherForm
from voucher.models import Invoice, PurchaseVoucher, InvoiceParticular, PurchaseParticular
from voucher.serializers import InvoiceSerializer, PurchaseVoucherSerializer
from django.http import HttpResponse
import json
from acubor.lib import delete_rows, invalid, save_model


def list_invoice(request):
    all_invoices = Invoice.objects.all()
    return render(request, 'list_invoice.html', {'invoices': all_invoices})


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
            new_invoice_no = int(last_invoice_no)+1
            invoice.invoice_no = "0" * (int(company_setting.invoice_digit_count) - str(new_invoice_no).__len__()) \
                                 + str(new_invoice_no)
        except:
            invoice.invoice_no = ''

    form = InvoiceForm(data=request.POST, instance=invoice)
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
    try:
        if params.get('id'):
            invoice = Invoice.objects.get(id=params.get('id'))
        else:
            invoice = Invoice()
            # if not created:
        invoice = save_model(invoice, invoice_values)
        dct['id'] = invoice.id
    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        else:
            dct['error_message'] = 'Error in form data!'
    model = InvoiceParticular
    for index, row in enumerate(params.get('particulars').get('rows')):
        if invalid(row, ['item_id', 'unit_price', 'quantity']):
            continue
        values = {'sn': index+1, 'item_id': row.get('item_id'), 'description': row.get('description'),
                  'unit_price': row.get('unit_price'), 'quantity': row.get('quantity'), 'discount': row.get('discount'),
                  'invoice': invoice}
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
        form = PurchaseVoucherForm(request.POST, request.FILES, instance=voucher)
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
                values = {'sn': index+1, 'item_id': row.get('item_id'), 'description': row.get('description'),
                          'unit_price': row.get('unit_price'), 'quantity': row.get('quantity'),
                          'discount': row.get('discount'), 'purchase_voucher': voucher}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
            delete_rows(particulars.get('deleted_rows'), model)

    else:
        form = PurchaseVoucherForm(instance=voucher)
    purchase_voucher_data = PurchaseVoucherSerializer(voucher).data
    return render(request, 'purchase_voucher.html', {'form': form, 'data': purchase_voucher_data})

