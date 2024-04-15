import json


def read_json_file(file_path:str)-> dict:
    """
    Read a JSON file and return its content as a Python dictionary.
    
    Args:
    - file_path (str): The path to the JSON file.
    
    Returns:
    - dict: The content of the JSON file as a dictionary.
    """
    try:
        with open(file_path, 'r') as json_file:
            json_content = json.load(json_file)
        return json_content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' is not a valid JSON file.")
        return None
    
def write_to_json_file(data, file_path):
    """
    Write data to a JSON file.
    
    Args:
    - data (dict): The data to be written, should be a dictionary.
    - file_path (str): The path to the JSON file to write.
    
    Returns:
    - bool: True if writing is successful, False otherwise.
    """
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return True
    except Exception as e:
        print(f"Error occurred while writing to file '{file_path}': {e}")
        return False