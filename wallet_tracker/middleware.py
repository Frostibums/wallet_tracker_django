import logging

from django.shortcuts import redirect

logger = logging.getLogger(__name__)


class ExceptionHandler(object):
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f'{exception}')
        return redirect('exception')
