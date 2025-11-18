
class Notify404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            from django.core.mail import mail_admins
            mail_admins(
                subject=f"404 on {request.path}",
                message=f"Someone hit a 404 at {request.build_absolute_uri()}"
            )
        return response
