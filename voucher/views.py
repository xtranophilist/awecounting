from forms import SalesVoucherForm
from models import SalesVoucher
from django.shortcuts import render
from voucher.serializers import SalesVoucherSerializer

def sales(request):
    sales_voucher = SalesVoucher()
    form = SalesVoucherForm(data=request.POST, instance=sales_voucher)
    voucher_data = SalesVoucherSerializer(sales_voucher).data
    voucher_data['read_only'] = {
        'invoice_prefix': 'INNV-',
        'invoice_suffix': '...',
    }
    return render(request, 'invoice.html', {'form': form, 'data': voucher_data})
