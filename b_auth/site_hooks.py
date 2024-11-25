from backend.hooks import NamedURLHook
from backend import hooks
from .urls import urlpatterns


@hooks.register('named_url_hook')
def register_patterns():
    return NamedURLHook(urlpatterns, "auth/")