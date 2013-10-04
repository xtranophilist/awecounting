from users.models import Role
from users.models import Company


class RoleMiddleware(object):
    def process_request(self, request):
        if not request.user.is_anonymous():
            roles = Role.objects.filter(user=request.user)
            if not request.session.get('company'):
                request.session['company'] = roles[0].company.id
            request.__class__.company = Company.objects.get(id=request.session['company'])
            request.__class__.roles = Role.objects.filter(user=request.user, company=request.company)
            groups = []
            for role in request.roles:
                groups.append(role.group)
            request.__class__.groups = groups
