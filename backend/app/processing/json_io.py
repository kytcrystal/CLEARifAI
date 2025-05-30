import json
import logging
logger = logging.getLogger(__name__)

def write_to_json(input_dict, file_prefix):
    try:
        output_path = file_prefix + ".json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(input_dict, f, indent=2, ensure_ascii=False)
        return output_path
    except Exception as e:
        logger.error(f"error writing to json file: {e}")
        raise

def load_json(file_path):
    try:
        with open(file_path, "r") as f:
            chunks = json.load(f)
        return chunks
    except Exception as e:
        logger.error(f"error loading file to json: {e}")
        raise