from users.models import Role
from users.models import Company


class CompanyMiddleware(object):
    def process_request(self, request):
        roles = Role.objects.filter(user=request.user)
        if not request.session.get('company'):
            request.session['company'] = roles[0].company.id
        request.__class__.company = Company.objects.get(id=request.session['company'])
        request.__class__.roles = roles
