from django.shortcuts import render
from tax.models import TaxScheme
from tax.serializers import TaxSchemeSerializer
from django.http import HttpResponse
import json


def index(request):
    tax_schemes = TaxScheme.objects.all()
    return render(request, 'tax_schemes.html', {'tax_schemes': tax_schemes})


def schemes_as_json(request):
    schemes = TaxScheme.objects.filter(company=request.user.company)
    items_data = TaxSchemeSerializer(schemes).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")
