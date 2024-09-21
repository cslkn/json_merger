import json
import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def fix_json_file():
    # Hide the root window
    Tk().withdraw()
    
    # Open file dialog to select JSON file
    file_path = askopenfilename(filetypes=[("JSON files", "*.json")])
    
    if not file_path:
        print("No file selected.")
        return
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Fix unquoted keys
    content = re.sub(r'(?<!")(\b\w+\b)(?=\s*:)', r'"\1"', content)
    
    # Fix unquoted values
    content = re.sub(r'(?<=:\s)(\b\w+\b)(?!")', r'"\1"', content)
    
    # Fix trailing commas
    content = re.sub(r',\s*([}\]])', r'\1', content)
    
    try:
        json_data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return
    
    with open(file_path, 'w') as file:
        json.dump(json_data, file, indent=4)
    
    print(f"Fixed JSON file saved at: {file_path}")

if __name__ == "__main__":
    fix_json_file()