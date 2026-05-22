import logging

_logger = logging.getLogger("northwind")


def log_request(request):
    # Redact the Authorization header before logging request metadata.
    headers = dict(request.headers)
    if "Authorization" in headers:
        headers["Authorization"] = "[redacted]"
    _logger.info("request path=%s account=%s headers=%s",
                 request.path, request.account.id, headers)
