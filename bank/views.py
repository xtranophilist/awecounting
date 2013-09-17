from datetime import date
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from bank.models import BankAccount, ChequeDeposit, ChequeDepositRow, BankCashDeposit, ChequePayment
from bank.forms import BankAccountForm, ChequeDepositForm, BankCashDepositForm, ChequePaymentForm
from acubor.lib import invalid, save_model
from ledger.models import delete_rows
from bank.serializers import ChequeDepositSerializer
from bank.filters import ChequeDepositFilter, CashDepositFilter, ChequePaymentFilter
from ledger.models import set_transactions, Account


@login_required
def list_bank_accounts(request):
    items = BankAccount.objects.filter(company=request.user.company)
    return render(request, 'list_bank_accounts.html', {'items': items})


@login_required
def delete_bank_account(request, id):
    object = get_object_or_404(BankAccount, id=id, company=request.user.company)
    object.delete()
    return redirect('/bank/accounts/')


@login_required
def delete_cheque_deposit(request, id):
    object = get_object_or_404(ChequeDeposit, id=id, company=request.user.company)
    object.delete()
    return redirect('/bank/cheque-deposits/')


@login_required
def delete_cash_deposit(request, id):
    object = get_object_or_404(BankCashDeposit, id=id, company=request.user.company)
    object.delete()
    return redirect('/bank/cash-deposits/')


@login_required
def delete_cheque_payment(request, id):
    object = get_object_or_404(ChequePayment, id=id, company=request.user.company)
    object.delete()
    return redirect('/bank/cheque-payments/')


@login_required
def list_cheque_deposits(request):
    items = ChequeDeposit.objects.filter(company=request.user.company)
    filtered_items = ChequeDepositFilter(request.GET, queryset=items, company=request.user.company)
    return render(request, 'list_cheque_deposits.html', {'objects': filtered_items})


@login_required
def list_cheque_payments(request):
    items = ChequePayment.objects.filter(company=request.user.company)
    filtered_items = ChequePaymentFilter(request.GET, queryset=items, company=request.user.company)
    return render(request, 'list_cheque_payments.html', {'objects': filtered_items})


@login_required
def list_cash_deposits(request):
    items = BankCashDeposit.objects.filter(company=request.user.company)
    filtered_items = CashDepositFilter(request.GET, queryset=items, company=request.user.company)
    return render(request, 'list_cash_deposits.html', {'objects': filtered_items})


@login_required
def bank_account_form(request, id=None):
    if id:
        bank_account = get_object_or_404(BankAccount, id=id, company=request.user.company)
        scenario = 'Update'
    else:
        bank_account = BankAccount()
        scenario = 'Create'
    if request.POST:
        form = BankAccountForm(data=request.POST, instance=bank_account)
        if form.is_valid():
            item = form.save(commit=False)
            item.company = request.user.company
            item.save()
            return redirect('/bank/accounts/')
    else:
        form = BankAccountForm(instance=bank_account)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'bank_account_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })


@login_required
def cheque_deposit(request, id=None):
    if id:
        receipt = get_object_or_404(ChequeDeposit, id=id, company=request.user.company)
        scenario = 'Update'
    else:
        receipt = ChequeDeposit(date=date.today())
        scenario = 'New'
    if request.POST:
        form = ChequeDepositForm(request.POST, request.FILES, instance=receipt, company=request.user.company)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.company = request.user.company
            if 'attachment' in request.FILES:
                receipt.attachment = request.FILES['attachment']
            receipt.save()
        if id or form.is_valid():
            particulars = json.loads(request.POST['particulars'])
            model = ChequeDepositRow
            bank_account = Account.objects.get(id=request.POST.get('bank_account'))
            benefactor = Account.objects.get(id=request.POST.get('benefactor'))
            for index, row in enumerate(particulars.get('rows')):
                if invalid(row, ['amount']):
                    continue
                values = {'sn': index + 1, 'cheque_number': row.get('cheque_number'),
                          'cheque_date': row.get('cheque_date'),
                          'drawee_bank': row.get('drawee_bank'), 'drawee_bank_address': row.get('drawee_bank_address'),
                          'amount': row.get('amount'), 'cheque_deposit': receipt}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                set_transactions(submodel, request.POST.get('date'),
                                 ['dr', bank_account, row.get('amount')],
                                 ['cr', benefactor, row.get('amount')],
                )
                if not created:
                    submodel = save_model(submodel, values)
            delete_rows(particulars.get('deleted_rows'), model)
            return redirect('/bank/cheque-deposits/')
    form = ChequeDepositForm(instance=receipt, company=request.user.company)
    receipt_data = ChequeDepositSerializer(receipt).data
    return render(request, 'cheque_deposit.html', {'form': form, 'data': receipt_data, 'scenario': scenario})


@login_required
def cash_deposit(request, id=None):
    if id:
        receipt = get_object_or_404(BankCashDeposit, id=id, company=request.user.company)
        scenario = 'Update'
    else:
        receipt = BankCashDeposit(date=date.today())
        scenario = 'New'
    if request.POST:
        form = BankCashDepositForm(request.POST, request.FILES, instance=receipt, company=request.user.company)

        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.company = request.user.company
            if 'attachment' in request.FILES:
                receipt.attachment = request.FILES['attachment']
            receipt.save()
            bank_account = Account.objects.get(id=request.POST.get('bank_account'))
            benefactor = Account.objects.get(id=request.POST.get('benefactor'))
            set_transactions(receipt, request.POST.get('date'),
                             ['dr', bank_account, request.POST.get('amount')],
                             ['cr', benefactor, request.POST.get('amount')],
            )
            return redirect('/bank/cash-deposits/')
    else:
        form = BankCashDepositForm(instance=receipt, company=request.user.company)
    return render(request, 'cash_deposit.html', {'form': form, 'scenario': scenario})


@login_required
def cheque_payment(request, id=None):
    if id:
        payment = get_object_or_404(ChequePayment, id=id, company=request.user.company)
        scenario = 'Update'
    else:
        payment = ChequePayment(date=date.today())
        scenario = 'New'
    if request.POST:
        form = ChequePaymentForm(request.POST, request.FILES, instance=payment, company=request.user.company)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.company = request.user.company
            print request.POST
            if 'attachment' in request.FILES:
                payment.attachment = request.FILES['attachment']
            payment.save()
            bank_account = Account.objects.get(id=request.POST.get('bank_account'))
            beneficiary = Account.objects.get(id=request.POST.get('beneficiary'))
            set_transactions(payment, request.POST.get('date'),
                             ['dr', bank_account, request.POST.get('amount')],
                             ['cr', beneficiary, request.POST.get('amount')],
            )
            return redirect('/bank/cheque-payments/')
    else:
        form = ChequePaymentForm(instance=payment, company=request.user.company)
    return render(request, 'cheque_payment.html', {'form': form, 'scenario': scenario})
