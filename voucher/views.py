from south.management.commands import patch_for_test_db_setup
from forms import InvoiceForm
from models import Invoice
from django.shortcuts import render, redirect
from voucher.serializers import InvoiceSerializer


def invoice(request):
    from core.models import CompanySetting
    try:
        company_setting = CompanySetting.objects.get(company=request.user.company)
    except CompanySetting.DoesNotExist:
        #TODO Add a flash message
        return redirect('/settings/company')
    sales_voucher = Invoice()
    form = InvoiceForm(data=request.POST, instance=sales_voucher)
    voucher_data = InvoiceSerializer(sales_voucher).data
    voucher_data['read_only'] = {
        'invoice_prefix': company_setting.invoice_prefix,
        'invoice_suffix': company_setting.invoice_suffix,
    }
    return render(request, 'invoice.html', {'form': form, 'data': voucher_data})

def save_invoice(request):
    import json
    params = json.loads(request.body)
    import pdb
    pdb.set_trace()
    # TODO process params

