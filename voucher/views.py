import json

from django.shortcuts import render, redirect

from forms import InvoiceForm, PurchaseVoucherForm
from voucher.models import Invoice, PurchaseVoucher
from voucher.serializers import InvoiceSerializer, PurchaseVoucherSerializer


def invoice(request, id=None):
    from core.models import CompanySetting
    try:
        company_setting = CompanySetting.objects.get(company=request.user.company)
    except CompanySetting.DoesNotExist:
        #TODO Add a flash message
        return redirect('/settings/company')
    invoice = Invoice()
    try:
        last_invoice = Invoice.objects.latest('id')
        new_invoice_no = int(last_invoice.invoice_no)+1
        invoice.invoice_no = "0" * (int(company_setting.invoice_digit_count) - str(new_invoice_no).__len__()) \
                             + str(new_invoice_no)
    except:
        invoice.invoice_no = ''
    invoice.currency = company_setting.default_currency
    form = InvoiceForm(data=request.POST, instance=invoice)
    invoice_data = InvoiceSerializer(invoice).data
    invoice_data['read_only'] = {
        'invoice_prefix': company_setting.invoice_prefix,
        'invoice_suffix': company_setting.invoice_suffix,
        }
    return render(request, 'invoice.html', {'form': form, 'data': invoice_data})


def save_invoice(request):
    params = json.loads(request.body)
    form = InvoiceForm(data=params, instance=Invoice())
    if form.is_valid():
        invoice = form.save(commit=False)
        # invoice.party_id = 1
        invoice.company = request.user.company
        invoice.save()
    else:
        print form.errors


def purchase_voucher(request, id=None):
    from core.models import CompanySetting
    try:
        company_setting = CompanySetting.objects.get(company=request.user.company)
    except CompanySetting.DoesNotExist:
        #TODO Add a flash message
        return redirect('/settings/company')
    purchase_voucher = PurchaseVoucher()
    form = PurchaseVoucherForm(data=request.POST, instance=purchase_voucher)
    purchase_voucher_data = PurchaseVoucherSerializer(purchase_voucher).data
    return render(request, 'purchase_voucher.html', {'form': form, 'data': purchase_voucher_data})

