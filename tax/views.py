from django.shortcuts import render
from models import TaxScheme


def index(request):
    tax_schemes = TaxScheme.objects.all()
    return render(request, 'tax_schemes.html', {'tax_schemes': tax_schemes})