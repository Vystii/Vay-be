from  .plugin_manager import DashboardBase
from django.utils.translation import gettext_lazy as _


class RequestBlock(DashboardBase):
    class Meta:
        abstract = False
    
    title = _("My requests")
    description = _("list of your requests")
    routeName = "home"
    icon = """
    <svg fill="CurrentColor" viewBox="0 0 100 100" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg"><path d="M73.3 69.4c-2.3-.9-2.6-1.8-2.6-2.8a3.6 3.6 0 0 1 1.4-2.6 6.42 6.42 0 0 0 2.1-5c0-3.8-2.3-7-6.3-7s-6.3 3.2-6.3 7a6.78 6.78 0 0 0 2.1 5 3.6 3.6 0 0 1 1.4 2.6c0 1-.3 1.9-2.6 2.9-3.3 1.5-6.4 3.3-6.5 6.3 0 2 1.5 4.1 3.4 4.1h17.2c1.9 0 3.4-2.1 3.2-4.1-.1-3-3.2-5-6.5-6.4"/><path d="M52 75.8v-.2c.2-5.4 5.2-8.1 8.2-9.5a10.53 10.53 0 0 1-2.6-7.1 12.6 12.6 0 0 1 .84-4.6H50.1a1.22 1.22 0 0 1-1.2-1.2v-2.3a1.22 1.22 0 0 1 1.2-1.2h12a10.58 10.58 0 0 1 11.15-.22V25.6A5.59 5.59 0 0 0 67.7 20H32.3a5.59 5.59 0 0 0-5.6 5.6v44.8a5.59 5.59 0 0 0 5.6 5.6H52zm-3.1-40.9a1.22 1.22 0 0 1 1.2-1.2h15.2a1.22 1.22 0 0 1 1.2 1.2v2.3a1.13 1.13 0 0 1-1.1 1.2H50.1a1.22 1.22 0 0 1-1.2-1.2Zm-4.1 20.5a.91.91 0 0 1 0 1.2l-1.2 1.2a.91.91 0 0 1-1.2 0L39 54.4l-3.3 3.3a.91.91 0 0 1-1.2 0l-1.2-1.2a.91.91 0 0 1 0-1.2l3.3-3.3-3.3-3.3a.91.91 0 0 1 0-1.2l1.2-1.2a.91.91 0 0 1 1.2 0l3.3 3.3 3.4-3.4a.91.91 0 0 1 1.2 0l1.2 1.2a.91.91 0 0 1 0 1.2L41.4 52Zm2.8-24.3-9 9a1.66 1.66 0 0 1-1.2.5 1.58 1.58 0 0 1-1.2-.5l-4.3-4.3a.75.75 0 0 1 0-1.2l1.2-1.2a.75.75 0 0 1 1.2 0l3.1 3.1 7.7-7.7a.75.75 0 0 1 1.2 0l1.2 1.2c.3.4.3 1 .1 1.1"/></svg>
    """
    active = True
    
    @staticmethod
    def getPluginInfos()->dict:
        return {
            "title": RequestBlock.title,
            "description": RequestBlock.description,
            "routeName": RequestBlock.routeName,
            "active": RequestBlock.active,
            "icon": RequestBlock.icon
        }    
    