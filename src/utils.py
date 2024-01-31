import re
from typing import Dict

def find_placeholders(task) -> set:
    placeholder_pattern = r'\$\{(\w+)\}' 
    placeholders = set()

    def search(obj):
        if isinstance(obj, dict):
            for value in obj.values():
                search(value)
        elif isinstance(obj, list):
            for item in obj:
                search(item)
        elif isinstance(obj, str):
            found = re.findall(placeholder_pattern, obj)
            placeholders.update(found)

    search(task)
    return placeholders

def replace_placeholders(obj, values) -> Dict:
    """Replace placeholders in a string, dict, or list with given values."""
    if isinstance(obj, str):
        for placeholder, value in values.items():
            obj = obj.replace(placeholder, value)
        return obj
    elif isinstance(obj, dict):
        return {k: replace_placeholders(v, values) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_placeholders(elem, values) for elem in obj]
    return obj