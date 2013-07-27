from forms import SalesVoucherForm
from models import SalesVoucher
from django.shortcuts import render
from voucher.serializers import SalesVoucherSerializer
from core.models import CompanySetting


def invoice(request):
    company_setting = CompanySetting.objects.get(company=request.user.company)
    sales_voucher = SalesVoucher()
    form = SalesVoucherForm(data=request.POST, instance=sales_voucher)
    voucher_data = SalesVoucherSerializer(sales_voucher).data
    voucher_data['read_only'] = {
        'invoice_prefix': company_setting.invoice_prefix,
        'invoice_suffix': company_setting.invoice_suffix,
    }
    return render(request, 'invoice.html', {'form': form, 'data': voucher_data})
