import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from tax.models import TaxScheme
from tax.serializers import TaxSchemeSerializer
from tax.forms import TaxSchemeForm
from django.contrib.auth.decorators import login_required

@login_required
def list_tax_schemes(request):
    tax_schemes = TaxScheme.objects.filter(company=request.user.company)
    return render(request, 'list_tax_schemes.html', {'objects': tax_schemes})

@login_required
def schemes_as_json(request):
    schemes = TaxScheme.objects.filter(company=request.user.company)
    items_data = TaxSchemeSerializer(schemes).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")

@login_required
def delete_tax_scheme(request, id):
    object = get_object_or_404(TaxScheme, id=id, company=request.user.company)
    object.delete()
    return redirect('/tax/schemes/')

@login_required
def tax_scheme_form(request, id=None):
    if id:
        object = get_object_or_404(TaxScheme, id=id, company=request.user.company)
        scenario = 'Update'
    else:
        object = TaxScheme(company=request.user.company)
        scenario = 'Create'
    if request.POST:
        form = TaxSchemeForm(data=request.POST, instance=object)
        if form.is_valid():
            object = form.save(commit=False)
            object.company = request.user.company
            object.save()
            return redirect('/tax/schemes/')
    else:
        form = TaxSchemeForm(instance=object)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'tax_scheme_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })