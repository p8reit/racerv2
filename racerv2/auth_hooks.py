from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook
from . import urls

class EmbedRacingMenu(MenuItemHook):
    def __init__(self):
        MenuItemHook.__init__(self,
                              'Embed Racing Dashboard',
                              'fas fa-flag-checkered fa-fw',  # Icon
                              'embed_racing:dashboard',  # Namespace and view name
                              navactive=['embed_racing:'])

    def render(self, request):
        if request.user.has_perm('embed_racing.view_trackedrequest'):
            return MenuItemHook.render(self, request)
        return ''

@hooks.register('menu_item_hook')
def register_menu():
    return EmbedRacingMenu()

@hooks.register('url_hook')
def register_url():
    return UrlHook(urls, 'embed_racing', '^embed_racing/')
