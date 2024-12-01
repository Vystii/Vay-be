from abc import abstractmethod
import inspect
import importlib
from django.conf import settings
    
    
class PluginBaseManager:
    class meta:
        abstract = True
    
    namespace = None
    def get_classes_in_namespace(cls, namespace):
        classes = []
        for name, obj in inspect.getmembers(namespace):
            if inspect.isclass(obj):
                if issubclass(obj, cls.getPluginBase()) and not obj.Meta.abstract:
                    classes.append(obj)
        return classes

    def check_and_get_classes(cls, apps):
        all_classes = {}
        for app in apps:
            try:
                subnamespace = importlib.import_module(f"{app}.{cls.getPluginsNamespace()}")
                print(subnamespace)
                classes = PluginBaseManager.get_classes_in_namespace(cls, subnamespace)
                all_classes[app] = classes
            except ModuleNotFoundError:
                all_classes[app] = []
        return all_classes
    
    @staticmethod
    @abstractmethod
    def getPluginsNamespace()->str:
        pass
    
    @staticmethod
    @abstractmethod
    def getPluginBase()->str:
        pass
    
    def getAllInstance(cls):
        """return all the class that extends a specific class

        Returns:
            list: classes that follow a certain logic ...
        """
        blocks = cls.check_and_get_classes(cls, settings.INSTALLED_APPS)
        return blocks