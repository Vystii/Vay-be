from abc import abstractmethod
from functools import wraps
from v_plugins.blocks.plugin_manager import PluginBaseManager


class DashboardBase:
    class Meta:
        abstract = True
    
    @staticmethod
    @abstractmethod
    def getPluginInfos():
        pass

class PluginManager(PluginBaseManager):
    class meta:
        abstract = False

    @staticmethod
    @wraps(PluginBaseManager.getAllInstances)
    def getAllInstances():
        return PluginBaseManager.getAllInstances(PluginManager)
    
    @staticmethod
    @wraps(PluginBaseManager.getAllInstances)
    def getBlocks() -> list[DashboardBase]:
        return PluginBaseManager.getBlocks(PluginManager)
    
    @staticmethod
    def getBlocksInfos()->list[dict]:
        return [block.getPluginInfos() for block in PluginManager.getBlocks()]
        
    @staticmethod 
    def getPluginsNamespace()->str:
        return "dashboard_block.dashboard_plugins"
    
    @staticmethod
    def getPluginBase():
        return DashboardBase