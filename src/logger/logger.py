import logging
from logging import StreamHandler
from typing import Any

from fastapi import Request


def init_logger(log_level: str):
    logger = logging.getLogger()
    logHandler = StreamHandler()
    logger.addHandler(logHandler)
    logger.setLevel(log_level)

    return logger


def request_logging(request: Request, body: dict | None = None) -> dict[str, Any]:
    path_params = request.path_params
    query_params = request.query_params
    endpoint_name = request.scope.get("endpoint", {})
    extra_args = {
        "method": request.method,
        "endpoint_url": request.url.path,
        "endpoint_name": endpoint_name
    }

    if body:
        extra_args["body"] = body
    if path_params:
        extra_args["path_params"] = path_params
    if query_params:
        extra_args["query_params"] = query_params

    return extra_args
