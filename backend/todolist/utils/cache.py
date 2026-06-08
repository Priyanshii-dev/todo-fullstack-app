from django.core.cache import cache
from urllib.parse import urlencode

CACHE_TIMEOUT = 300  # 5 minutes


def get_user_tasks_cache_key(user_id, params=None):
    base = f"user_tasks:{user_id}"
    if not params:
        return base
    # Build a stable, deterministic key from sorted query params
    filtered = {k: params.get(k, "") for k in ("page", "limit", "search", "status")}
    return f"{base}:{urlencode(sorted(filtered.items()))}"


def clear_user_tasks_cache(user_id):
    # django-redis supports delete_pattern; clears all page/filter variants
    cache.delete_pattern(f"user_tasks:{user_id}:*")
    cache.delete(f"user_tasks:{user_id}")
