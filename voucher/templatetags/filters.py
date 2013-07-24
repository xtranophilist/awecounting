from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.template import Library
from django.utils.safestring import mark_safe
from django.db.models import Model
# from django.forms.models import model_to_dict

register = Library()


@register.filter
def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    if isinstance(object, Model):
        return mark_safe(serialize('json', [object, ]))
    return mark_safe(simplejson.dumps(object))


@register.filter
def user_to_json(user):
    if hasattr(user, '_wrapped') and hasattr(user, '_setup'):
            if user._wrapped.__class__ == object:
                user._setup()
            user = user._wrapped
    user_dict = {'id': user.id, 'username': user.username}
    return mark_safe(simplejson.dumps(user_dict))


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
