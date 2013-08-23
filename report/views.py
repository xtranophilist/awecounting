from django.http import HttpResponse
import json
from django.shortcuts import render, get_object_or_404, redirect


def trial_balance(request):
    return render(request, 'trial_balance.html', {
        # 'tax_schemes': tax_schemes
    })
