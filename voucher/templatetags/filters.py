import json
from datetime import date, timedelta

from django.core import serializers
from django.db.models.query import QuerySet
from django.template import Library
from django.utils.safestring import mark_safe
from django.db.models import Model


register = Library()


def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    # elif isinstance(obj, ...):
    #     return ...
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))


@register.filter
def jsonify(object):
    if isinstance(object, QuerySet):
        return serializers.serialize('json', object)
    if isinstance(object, Model):
        model_dict = object.__dict__
        del model_dict['_state']
        return mark_safe(json.dumps(model_dict))
    return mark_safe(json.dumps(object, default=handler))


@register.filter
def user_to_json(user):
    if hasattr(user, '_wrapped') and hasattr(user, '_setup'):
        if user._wrapped.__class__ == object:
            user._setup()
        user = user._wrapped
    user_dict = {'id': user.id, 'username': user.username}
    return mark_safe(json.dumps(user_dict))


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def remove_account(transactions, account):
    return [transaction for transaction in transactions if
            transaction.account.id is not account.id and (
                transaction.dr_amount or transaction.cr_amount)]


@register.filter
def if_not_none(obj):
    if obj is None:
        return ''
    return obj


@register.filter
def subtract(value, arg):
    if value is None:
        value = 0
    if arg is None:
        arg = 0
    return value - arg


@register.filter
def url_for_content(obj):
    #TODO DB Optimisation
    try:
        source = obj.content_type.get_object_for_this_type(id=obj.model_id)
    except:
        return None
    return source.get_absolute_url()


@register.filter
def dr_or_cr(val):
    if val < 0:
        return str(val * -1) + ' (Cr)'
    else:
        return str(val) + ' (Dr)'


@register.simple_tag
def yesterday():
    today = date.today()
    yesterday = today - timedelta(days=1)
    return yesterday

@register.filter
def day_journal_id(obj):
    #TODO DB Optimisation
    try:
        source = obj.content_type.get_object_for_this_type(id=obj.model_id)
    except:
        return None
    try:
        return source.day_journal.id
    except:
        return source.id