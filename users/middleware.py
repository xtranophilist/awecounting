from users.models import Role


class CompanyMiddleware(object):
    def process_request(self, request):
        if not request.session.get('company'):
            request.session['company'] = Role.objects.filter(user=request.user)[0].company.id
        request.__class__.company = request.session['company']
