from django.shortcuts import render, redirect
from core.models import CompanySetting, Category
from ledger.models import Party
from core.forms import CompanySettingsForm, PartyForm, CategoryForm
from django.shortcuts import render, get_object_or_404


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


def party_form(request, id=None):
    if id:
        party = get_object_or_404(Party, id=id)
    else:
        party = Party()
    if request.POST:
        form = PartyForm(data=request.POST, instance=party)
        if form.is_valid():
            party = form.save(commit=False)
            party.company = request.user.company
            party.save()
    else:
        form = PartyForm(instance=party)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'party_form.html', {
        'form': form,
        'base_template': base_template,
    })


def list_categories(request):
    categories = Category.objects.filter(company=request.user.company)
    return render(request, 'list_categories.html', {'categories': categories})


def create_category(request):
    category = Category()
    if request.POST:
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.company = request.user.company
            category.save()
            return redirect('/categories/')
    else:
        form = CategoryForm(instance=category)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'category_create_form.html', {
        'form': form,
        'base_template': base_template,
    })


def update_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.POST:
        form = CategoryForm(data=request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.company = request.user.company
            category.save()
            return redirect('/categories/')
    else:
        form = CategoryForm(instance=category)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'category_update_form.html', {
        'form': form,
        'base_template': base_template
    })


def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('/categories/')
