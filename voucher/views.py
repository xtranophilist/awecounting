from forms import SalesVoucherForm
from models import SalesVoucher
from django.shortcuts import render

def sales(request):
    sales_voucher = SalesVoucher()
    form = SalesVoucherForm(data=request.POST, instance=sales_voucher)
    return render(request, 'sales_voucher.html', {"form": form})
