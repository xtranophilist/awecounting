import json

from django.shortcuts import render, redirect
from datetime import date

from forms import InvoiceForm, PurchaseVoucherForm
from voucher.models import Invoice, PurchaseVoucher, Particular
from voucher.serializers import InvoiceSerializer, PurchaseVoucherSerializer
from django.http import HttpResponse
import json
from journal.views import invalid, get_journal, save_model, delete_rows


def invoice(request, id=None):
    from core.models import CompanySetting
    try:
        company_setting = CompanySetting.objects.get(company=request.user.company)
    except CompanySetting.DoesNotExist:
        #TODO Add a flash message
        return redirect('/settings/company')
    if id:
        invoice = Invoice.objects.get(id=id)
    else:
        invoice = Invoice()
    try:
        print 'hi'
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
    invoice.currency = company_setting.default_currency
    invoice.date = date.today()
    form = InvoiceForm(data=request.POST, instance=invoice)
    invoice_data = InvoiceSerializer(invoice).data
    invoice_data['read_only'] = {
        'invoice_prefix': company_setting.invoice_prefix,
        'invoice_suffix': company_setting.invoice_suffix,
        }
    return render(request, 'invoice.html', {'form': form, 'data': invoice_data})


def save_invoice(request):
    params = json.loads(request.body)
    dct = {}
    invoice_values = {'party_id': params.get('party'), 'invoice_no': params.get('invoice_no'),
                      'reference': params.get('reference'), 'date': params.get('date'),
                      'due_date': params.get('due_date'), 'tax': params.get('tax'),
                      'currency_id': params.get('currency'), 'company': request.user.company}

    try:
        if params.get('id'):
            # invoice, created = Invoice.objects.get_or_create(id=params.get('id'), defaults=invoice_values)
            invoice = Invoice.objects.get(id=params.get('id'))
        else:
            invoice = Invoice()
            # if not created:
        invoice = save_model(invoice, invoice_values)
    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        else:
            dct['error_message'] = 'Error in form data!'
    model = Particular
    for index, row in enumerate(params.get('particulars').get('rows')):
        print row
        if invalid(row, ['item_id', 'unit_price', 'quantity']):
            continue
        values = {'sn': index+1, 'item_id': row.get('item_id'), 'description': row.get('description'),
                  'unit_price': row.get('unit_price'), 'quantity': row.get('quantity'), 'invoice': invoice}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct[index] = submodel.id
    delete_rows(params.get('particulars').get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def purchase_voucher(request, id=None):
    from core.models import CompanySetting
    try:
        company_setting = CompanySetting.objects.get(company=request.user.company)
    except CompanySetting.DoesNotExist:
        #TODO Add a flash message
        return redirect('/settings/company')
        # return HttpResponseRedirect(reverse('myapp.views.list'))
    if request.POST:
        form = PurchaseVoucherForm(request.POST, request.FILES)
        import pdb
        pdb.set_trace()
        if form.is_valid():
            voucher = form.save(commit=False)
            voucher.attachment = request.FILES['attachment']
            voucher.company = request.user.company
            voucher.save()
    purchase_voucher = PurchaseVoucher()
    form = PurchaseVoucherForm(data=request.POST, instance=purchase_voucher)
    purchase_voucher_data = PurchaseVoucherSerializer(purchase_voucher).data
    return render(request, 'purchase_voucher.html', {'form': form, 'data': purchase_voucher_data})

