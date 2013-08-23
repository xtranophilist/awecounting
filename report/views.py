from django.http import HttpResponse
import json
from django.shortcuts import render, get_object_or_404, redirect
from ledger.models import Category
from mptt.templatetags.mptt_tags import cache_tree_children


def recursive_node_to_dict(node):
    result = {
        'id': node.pk,
        'name': node.name,
    }
    children = [recursive_node_to_dict(c) for c in node.get_children()]
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
    dicts = to_dict(Category)
    print json.dumps(dicts, indent=4)
    return render(request, 'trial_balance.html', {
        'categories': categories
    })
