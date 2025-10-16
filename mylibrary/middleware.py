from django.conf import settings
from django.http import JsonResponse


class ApiKeyMiddleware:
    """Global guard for API endpoints under /api/.

    Denies access unless the provided key (header X-API-Key or query param api_key)
    matches settings.API_KEY. If settings.API_KEY is empty, API is disabled.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info or request.path
        if path.startswith('/api/'):
            configured = getattr(settings, 'API_KEY', '').strip()
            if not configured:
                return JsonResponse({'detail': 'API access disabled'}, status=401)

            provided = request.headers.get('X-API-Key') or request.META.get('HTTP_X_API_KEY') or request.GET.get('api_key') or ''
            if provided.strip() != configured:
                return JsonResponse({'detail': 'Invalid or missing API key'}, status=401)

        return self.get_response(request)
