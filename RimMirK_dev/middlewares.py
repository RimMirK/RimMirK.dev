import os
import traceback
from django.conf import settings
from django.core.mail import mail_admins

LOG_TAIL_LINES = os.environ["LOG_TAIL_LINES"]
LOG_FILE_PATH  = os.environ["LOG_FILE_PATH"]

class Notify404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            debug_info = self._build_debug_info(request)
            mail_admins(
                subject=f"404 on {request.path}",
                message=debug_info
            )

        return response

    def _build_debug_info(self, request):
        lines = []

        # 1) Общая инфа
        lines.append(f"URL: {request.build_absolute_uri()}")
        lines.append(f"Method: {request.method}")
        lines.append(f"GET params: {dict(request.GET)}")
        lines.append(f"POST params: {dict(request.POST)}")

        # 2) Файл, который пытались загрузить
        file_info = self._detect_file(request.path)
        if file_info:
            lines.append(f"Static/Media file resolved: {file_info}")
        else:
            lines.append("Static/Media file: no match")

        # 3) User
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            lines.append(f"User: {user} (id={user.id})")
        else:
            lines.append("User: anonymous")

        # 4) Headers
        ua = request.META.get("HTTP_USER_AGENT", "")
        ref = request.META.get("HTTP_REFERER", "")
        ip = request.META.get("REMOTE_ADDR", "")

        lines.append(f"User-Agent: {ua}")
        lines.append(f"Referer: {ref}")
        lines.append(f"IP: {ip}")

        # 5) META
        lines.append("\nMETA:")
        for k, v in request.META.items():
            lines.append(f"  {k}: {v}")

        # 6) Последние строки лога
        lines.append("\nLOG TAIL:")
        lines.append(self._tail_log())

        return "\n".join(lines)

    def _detect_file(self, path):
        """
        Пытаемся понять: искали static или media файл.
        """
        static_url = getattr(settings, "STATIC_URL", "/static/")
        media_url = getattr(settings, "MEDIA_URL", "/media/")

        # STATIC
        if static_url and path.startswith(static_url):
            relative = path[len(static_url):]
            return os.path.join(getattr(settings, "STATIC_ROOT", ""), relative)

        # MEDIA
        if media_url and path.startswith(media_url):
            relative = path[len(media_url):]
            return os.path.join(getattr(settings, "MEDIA_ROOT", ""), relative)

        return None

    def _tail_log(self):
        """
        Возвращает последние N строк из LOG_FILE_PATH.
        """
        if not os.path.exists(LOG_FILE_PATH):
            return f"Log file not found: {LOG_FILE_PATH}"

        try:
            with open(LOG_FILE_PATH, "rb") as f:
                f.seek(0, os.SEEK_END)
                size = f.tell()

                block = 2048
                data = b""
                while len(data.splitlines()) <= LOG_TAIL_LINES and f.tell() > 0:
                    step = min(block, f.tell())
                    f.seek(-step, os.SEEK_CUR)
                    data = f.read(step) + data
                    f.seek(-step, os.SEEK_CUR)

                lines = data.splitlines()[-LOG_TAIL_LINES:]
                return b"\n".join(lines).decode(errors="replace")

        except Exception as e:
            return f"Error reading log file: {e}"
