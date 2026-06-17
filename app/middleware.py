from django.core.cache import cache
from django.http import JsonResponse
import time

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.path.startswith('/restricted-area/'):
            
            ip_address = request.META.get('REMOTE_ADDR')
            cache_key = f"rate_limit_{ip_address}"
            
            
            request_history = cache.get(cache_key, [])
            current_time = time.time()
            
            
            request_history = [t for t in request_history if current_time - t < 60]
            
            if len(request_history) >= 5:
                
                return JsonResponse(
                    {"error": "Too many requests. Лимит 5 запросов в минуту."}, 
                    status=429
                )
            
            
            request_history.append(current_time)
            cache.set(cache_key, request_history, timeout=60)
            
        response = self.get_response(request)
        return response
