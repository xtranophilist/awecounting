from django.shortcuts import render
from ledger.models import Category
from mptt.templatetags.mptt_tags import cache_tree_children


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


def to_dict(model):
    root_nodes = cache_tree_children(model.objects.all())
    dicts = []
    for n in root_nodes:
        dicts.append(recursive_node_to_dict(n))
    return dicts


def trial_balance(request):
    categories = Category.objects.filter(company=request.user.company)

    dict = {
        'categories': to_dict(Category)
    }
    return render(request, 'trial_balance.html', {
        'dict': dict,
        'categories': categories
    })
