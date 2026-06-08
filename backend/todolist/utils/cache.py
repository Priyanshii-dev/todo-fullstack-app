from django.core.cache import cache

CACHE_TIMEOUT = 300  # 5 minutes


def get_user_tasks_cache_key(user_id):
    return f"user_tasks:{user_id}"


def clear_user_tasks_cache(user_id):
    cache.delete(get_user_tasks_cache_key(user_id))