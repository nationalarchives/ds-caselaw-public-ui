"""
Middleware for VCR cassette recording/playback.
"""

import logging

from .vcr_config import VCR_ENABLED, VCR_MODE, VCRContext

logger = logging.getLogger(__name__)


class VCRMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.vcr_context = None

    def __call__(self, request):
        if not VCR_ENABLED:
            return self.get_response(request)

        cassette_name = self._generate_cassette_name(request)

        try:
            with VCRContext.for_request(request.method, request.path, request.META.get("QUERY_STRING", "")):
                response = self.get_response(request)
            return response
        except Exception as e:
            logger.warning(f"VCR error for cassette {cassette_name} in {VCR_MODE} mode: {e}")
            if VCR_MODE == "record":
                logger.error("Failed to record cassette, attempting without VCR")
            raise

    def _generate_cassette_name(self, request):
        method = request.method.lower()
        path = request.path.strip("/").replace("/", "_")

        cassette_name = f"{path}_{method}"
        cassette_name = cassette_name.replace("-", "_")

        if len(cassette_name) > 100:
            cassette_name = cassette_name[:100]

        return cassette_name
