from django.shortcuts import render
from mptt.templatetags.mptt_tags import cache_tree_children
from django.contrib.auth.decorators import login_required

from ledger.models import Category


def recursive_node_to_dict(node):
    result = {
        'id': node.pk,
        'name': node.name,
    }
    children = [recursive_node_to_dict(c) for c in node.get_children()]
    accounts = []
    for account in node.accounts.all():
        a = {'id': account.id, 'code': account.code, 'name': account.name, 'dr': account.current_dr,
             'cr': account.current_cr}
        accounts.append(a)
    result['accounts'] = accounts
    if children:
        result['children'] = children
    return result


def to_dict(model, company):
    root_nodes = cache_tree_children(model.objects.filter(company=company))
    dicts = []
    for n in root_nodes:
        dicts.append(recursive_node_to_dict(n))
    return dicts


@login_required
def trial_balance(request):
    categories = Category.objects.filter(company=request.user.company)

    dict = {
        'categories': to_dict(Category, request.user.company)
    }
    # print request.get
    return render(request, 'trial_balance.html', {
        'dict': dict,
        'categories': categories
    })
