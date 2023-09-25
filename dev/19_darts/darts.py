HOME = os.getenv('HOME')
DARTS_PATH = os.path.join(HOME, '/Work/blog/dev/19_darts/')
import base64
import io
import json
import os
from pathlib import Path

from PIL import Image


def get_image_and_labels(json_file):
    
    with open(os.path.join(DARTS_PATH, f'images/{json_file}')) as f:
        data = json.load(f)
        
    filtered_labels = [x for x in data['shapes'] if x['label'] == '3']  # 3 is just the label for the lines I had
    points = [x['points'][1] for x in filtered_labels]   # and I select 1 as the tip of the dart
    
    # Decode the Base64 string
    image_data = base64.b64decode(data["imageData"])

    # Convert to a PIL Image
    image = Image.open(io.BytesIO(image_data))
    
    return image, points