from django.utils.deprecation import MiddlewareMixin

from backends.settings import UN_LOG_PATH_PREFIX
from utils.log_write import handle_request, handle_response


class LogMiddleware(MiddlewareMixin):

    @classmethod
    def process_request(cls, request):
        data = getattr(request, '_body', request.body)
        request._body = data
        return None

    @classmethod
    def process_response(cls, request, response):
        path = request.path
        try:
            path_prefix = path.split("/")[1]
            path_prefix2 = path.split("/")[2]
        except Exception:
            path_prefix = ''
            path_prefix2 = ''

        if path_prefix not in UN_LOG_PATH_PREFIX and path_prefix2 not in UN_LOG_PATH_PREFIX:
            handle_request(request)
            handle_response(response)

        return response
