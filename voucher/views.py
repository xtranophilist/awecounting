from forms import SalesVoucherForm
from models import SalesVoucher
from django.shortcuts import render
from voucher.serializers import SalesVoucherSerializer

def sales(request):
    sales_voucher = SalesVoucher()
    sales_voucher.reference = 'a'
    form = SalesVoucherForm(data=request.POST, instance=sales_voucher)
    voucher_data = SalesVoucherSerializer(sales_voucher).data
    return render(request, 'sales_voucher.html', {'form': form, 'data': voucher_data})
