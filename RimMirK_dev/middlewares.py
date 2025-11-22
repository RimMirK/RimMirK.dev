import traceback
from django.core.mail import mail_admins
from django.http import Http404

class Notify404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Http404 as e:
            # Если 404 была вызвана исключением — ловим тут
            debug_info = self._build_debug_info(request, error=e)
            mail_admins(
                subject=f"404 (exception) on {request.path}",
                message=debug_info
            )
            raise

        if response.status_code == 404:
            # Обычная 404 без исключения
            debug_info = self._build_debug_info(request, error=None)
            mail_admins(
                subject=f"404 on {request.path}",
                message=debug_info
            )

        return response

    def _build_debug_info(self, request, error=None):
        lines = []

        # Общая инфа
        lines.append(f"URL: {request.build_absolute_uri()}")
        lines.append(f"Method: {request.method}")
        lines.append(f"GET params: {dict(request.GET)}")
        lines.append(f"POST params: {dict(request.POST)}")

        # Юзер
        user = request.user if hasattr(request, "user") else None
        if user and user.is_authenticated:
            lines.append(f"User: {user} (id={user.id})")
        else:
            lines.append("User: anonymous")

        # Заголовки
        ua = request.META.get("HTTP_USER_AGENT", "")
        ref = request.META.get("HTTP_REFERER", "")
        ip = request.META.get("REMOTE_ADDR", "")

        lines.append(f"User-Agent: {ua}")
        lines.append(f"Referer: {ref}")
        lines.append(f"IP: {ip}")

        # Полный META
        lines.append("\nMETA:")
        for k, v in request.META.items():
            lines.append(f"  {k}: {v}")

        # Ошибка, если была
        if error is not None:
            lines.append("\nException:")
            lines.append(f"{repr(error)}")
            lines.append("Traceback:")
            tb = traceback.format_exc()
            lines.append(tb)

        return "\n".join(lines)
