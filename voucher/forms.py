from acubor.lib import KOModelForm
from models import SalesVoucher


class SalesVoucherForm(KOModelForm):

    class Meta:
        model = SalesVoucher
