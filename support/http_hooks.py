import logging

from requests import Response

logger = logging.getLogger(__name__)


def raise_for_status_hook(response: Response, *args, **kwargs):
    response.raise_for_status()
