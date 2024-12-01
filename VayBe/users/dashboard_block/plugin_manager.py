from abc import abstractmethod
from v_plugins.blocks.plugin_manager import PluginBaseManager


class DashboardBase:
    class Meta:
        abstract = True
    
    @staticmethod
    @abstractmethod
    def getPluginInfo():
        pass

class PluginManager(PluginBaseManager):
    class meta:
        abstract = False
            
    @staticmethod 
    def getPluginsNamespace()->str:
        return "dashboard_block.dashboard_plugins"
    
    @staticmethod
    def getPluginBase():
        return DashboardBase