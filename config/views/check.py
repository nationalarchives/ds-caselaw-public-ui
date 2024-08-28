from django.http import JsonResponse

from judgments.utils.utils import get_document_by_uri_from_cache


def status(request):
    document_cache_info = get_document_by_uri_from_cache.cache_info()

    return JsonResponse(
        {
            "status": "OK",
            "document_cache": {
                "hits": document_cache_info.hits,
                "misses": document_cache_info.misses,
                "current_size": document_cache_info.currsize,
                "max_size": document_cache_info.maxsize,
            },
        }
    )
