import os
import json
from tkinter import Tk
from tkinter.filedialog import askdirectory

def merge_json_files_in_directory():
    # Hide the root Tkinter window
    Tk().withdraw()
    
    # Open a dialog to select a directory
    directory = askdirectory(title="Select a folder containing JSON files")
    
    if not directory:
        print("No directory selected.")
        return
    
    merged_data = []
    
    # Iterate over all files in the selected directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                merged_data.append(data)
    
    # Write the merged data to a new JSON file in the project directory
    output_file_path = os.path.join(os.getcwd(), 'merged_json.json')
    with open(output_file_path, 'w') as output_file:
        json.dump(merged_data, output_file, indent=4)
    
    print(f"Merged JSON file created at: {output_file_path}")

if __name__ == "__main__":
    merge_json_files_in_directory()