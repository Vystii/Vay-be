from abc import abstractmethod
from functools import wraps
from v_plugins.blocks.plugin_manager import PluginBaseManager
from v_utilities.urls import route_exists

class DashboardBase:
    class Meta:
        abstract = True
    weight = 0    
    @staticmethod
    def getPluginInfos(cls)->dict:
        return {
            "title": cls.title,
            "description": cls.description,
            "route_name": cls.routeName,
            "active": cls.active,
            "icon": cls.icon,
            "weight" : cls.weight
        }

class PluginManager(PluginBaseManager):
    class meta:
        abstract = False

    @staticmethod
    @wraps(PluginBaseManager.getAllInstances)
    def getAllInstances():
        element = PluginBaseManager.getAllInstances(PluginManager)[0]["weight"]
        data = sorted(PluginBaseManager.getAllInstances(PluginManager), key=lambda plugin: plugin["weight"])
        return [] 
    
    @staticmethod
    @wraps(PluginBaseManager.getAllInstances)
    def getBlocks() -> list[DashboardBase]:
        data =  PluginBaseManager.getBlocks (PluginManager)
        return data
    
    @staticmethod
    def getBlocksInfos()->list[dict]:
        
        return sorted([block.getPluginInfos() for block in PluginManager.getBlocks()], key = lambda plugin    : plugin["weight"])
        
    @staticmethod 
    def getPluginsNamespace()->str:
        return "dashboard_block.dashboard_plugins"
    
    @staticmethod
    def getPluginBase():
        return DashboardBase