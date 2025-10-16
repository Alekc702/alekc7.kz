from functools import wraps
from django.conf import settings
from django.http import JsonResponse, HttpRequest, HttpResponse


def _extract_api_key(request: HttpRequest) -> str:
    """Return API key from header 'X-API-Key' or query param 'api_key'."""
    header_key = request.headers.get('X-API-Key') or request.META.get('HTTP_X_API_KEY')
    if header_key:
        return header_key.strip()
    return (request.GET.get('api_key') or '').strip()


def api_key_required(view_func):
    """
    Decorator to require a static API key for JSON endpoints.
    If settings.API_KEY is empty, deny access by default.
    """

    @wraps(view_func)
    def _wrapped(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        configured = getattr(settings, 'API_KEY', '').strip()
        provided = _extract_api_key(request)

        if not configured:
            return JsonResponse({'detail': 'API access disabled'}, status=401)

        if provided != configured:
            return JsonResponse({'detail': 'Invalid or missing API key'}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped
