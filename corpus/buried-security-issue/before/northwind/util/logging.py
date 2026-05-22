import logging

_logger = logging.getLogger("northwind")


def log_request(request):
    _logger.info("request path=%s account=%s", request.path, request.account.id)
