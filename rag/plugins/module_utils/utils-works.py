import json
import os 
import pkgutil

def load_config():
    #config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    # Check if the file exists
    #if not os.path.isfile(config_path):
    #    raise FileNotFoundError(f"Config file not found at {config_path}")
    #config_path = pkgutil.get_data('ansible_collections.ceemea.rag.plugins.module_utils', 'config.json')
    with open('/Users/livigni/Documents/TNC/WCA4A/clients/CAGIP/playbooks/cagip/uc4/ansible_collections/ceemea/rag/plugins/module_utils/config.json', 'r') as config_file:
    #with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config