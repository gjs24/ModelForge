# generator/services/model_generator.py

import json
from django.core.files.base import ContentFile

def generate_json_model(instance):
    """
    Takes a GeneratedModel instance
    Generates a JSON file
    Returns a Django ContentFile
    """

    data = {
        "name": instance.name,
        "type": instance.model_type,
        "dimensions": {
            "width": instance.width,
            "height": instance.height,
            "depth": instance.depth
        },
        "created_at": instance.created_at.isoformat()
    }

    json_content = json.dumps(data, indent=4)

    filename = f"{instance.name.replace(' ', '_').lower()}.json"

    return filename, ContentFile(json_content)
