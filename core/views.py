from django.shortcuts import render, redirect
from core.models import CompanySetting
from core.forms import CompanySettingsForm


def company_settings(request):
    try:
        company_setting = CompanySetting.objects.get(company=request.user.company)
    except CompanySetting.DoesNotExist:
        try:
            company_setting = CompanySetting(company=request.user.company)
        except ValueError:
            raise Exception("User doesn't have a company!")
    if request.POST:
        form = CompanySettingsForm(data=request.POST, instance=company_setting)
        if form.is_valid():
            form.save()
    else:
        form = CompanySettingsForm(instance=company_setting)
    return render(request, 'company_settings.html', {'company_setting': company_setting, 'form': form})
