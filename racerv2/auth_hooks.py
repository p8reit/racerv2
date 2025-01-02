from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook
from . import urls

class EmbedRacingMenu(MenuItemHook):
    def __init__(self):
        MenuItemHook.__init__(self,
                              'Racer Dashboard',
                              'fas fa-flag-checkered fa-fw',  # Icon
                              'racerv2:dashboard',  # Correct namespace
                              navactive=['racerv2:'])  # Correct navactive prefix

    def render(self, request):
        if request.user.has_perm('racerv2.view_trackedrequest'):
            return MenuItemHook.render(self, request)
        return ''

@hooks.register('menu_item_hook')
def register_menu():
    return EmbedRacingMenu()

@hooks.register('url_hook')
def register_url():
    return UrlHook(urls, 'racerv2', '^racerv2/')  # Correct namespace and prefix
