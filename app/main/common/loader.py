from typing import Dict, Any

import yaml


def load_yaml(yaml_file: str) -> Dict[str, Any]:
    with open(yaml_file, 'r') as f:
        yaml_config = yaml.safe_load(f)

    return yaml_config
