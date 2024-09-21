import os
import json
import tkinter as tk
from tkinter import filedialog

def split_json_file():
    # Create a Tkinter root window and hide it
    root = tk.Tk()
    root.withdraw()

    # Open a file dialog to select a JSON file
    file_path = filedialog.askopenfilename(
        title="Select a JSON file",
        filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
    )

    if not file_path:
        print("No file selected.")
        return

    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Determine the size of each split
    total_items = len(data)
    split_size = total_items // 10

    # Create the output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(file_path), "split_json_files")
    os.makedirs(output_dir, exist_ok=True)

    # Split the JSON data and write to new files
    for i in range(10):
        start_index = i * split_size
        end_index = (i + 1) * split_size if i < 9 else total_items
        split_data = data[start_index:end_index]

        output_file_path = os.path.join(output_dir, f"split_{i + 1}.json")
        with open(output_file_path, 'w') as output_file:
            json.dump(split_data, output_file, indent=4)

    print(f"JSON file split into 10 parts and saved in {output_dir}")

if __name__ == "__main__":
    split_json_file()