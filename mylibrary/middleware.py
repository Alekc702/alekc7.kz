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

            # Try query param first (no header-based key support)
            provided = request.GET.get('api_key') or ''

            # Also support path token for games list: /api/games/<key> or /api/games/<key>/
            if not provided and (path.startswith('/api/games/') and len(path) > len('/api/games/')):
                rest = path[len('/api/games/'):]
                # Extract first segment before '/'
                segment = rest.split('/', 1)[0]
                if segment:
                    provided = segment
            if provided.strip() != configured:
                return JsonResponse({'detail': 'Invalid or missing API key'}, status=401)

            # Mark request as API-authenticated for downstream decorators/views
            try:
                request._api_key_authenticated = True  # type: ignore[attr-defined]
            except Exception:
                pass

        return self.get_response(request)
