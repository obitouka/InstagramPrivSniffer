import os
import importlib
from plugins.base import ProviderPlugin

def load_plugins():
    """
    Dynamically loads all plugins from the 'plugins' directory.
    Returns a dictionary of plugin instances, keyed by their names.
    """
    plugins = {}
    plugin_dir = "plugins"
    for filename in os.listdir(plugin_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"{plugin_dir}.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if isinstance(item, type) and issubclass(item, ProviderPlugin) and item is not ProviderPlugin:
                        plugin_instance = item()
                        plugins[plugin_instance.name] = plugin_instance
            except Exception as e:
                print(f"Could not load plugin {module_name}: {e}")
    return plugins
