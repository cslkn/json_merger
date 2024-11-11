import os
import json
import tkinter as tk
from tkinter import messagebox

def load_games_data(directory):
    games_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                games_data[filename] = json.load(f)
    return games_data

def display_games(wyscout_filename):
    global wyscout_data  # Declare wyscout_data as global

    # Clear previous checkboxes and labels
    for widget in frame.winfo_children():
        widget.destroy()

    wyscout_file_path = os.path.join(wyscout_directory, wyscout_filename)
    games_file_path = os.path.join(games_directory, wyscout_filename)

    # Load Wyscout data
    with open(wyscout_file_path, 'r') as f:
        wyscout_data = json.load(f)

    # Check for the corresponding games data
    if os.path.exists(games_file_path):
        with open(games_file_path, 'r') as f:
            games_data = json.load(f)
    else:
        messagebox.showinfo("File Missing", f"Skipping {wyscout_filename} because corresponding games file does not exist.")
        return  # Skip displaying this file if games file does not exist

    # Sort games by team names
    wyscout_data.sort(key=lambda g: (g['home_team'], g['away_team']))
    games_data.sort(key=lambda g: (g['home_team'], g['away_team']))

    # Display Wyscout games on the left
    tk.Label(frame, text="Wyscout Games", font=('Arial', 14, 'bold')).grid(row=0, column=0, padx=10, pady=10)
    for i, game in enumerate(wyscout_data):
        wyscout_id = game['wyId']
        home_team = game['home_team']
        away_team = game['away_team']
        home_score = game['home_score']
        away_score = game['away_score']

        # Create a checkbox for each Wyscout game
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(frame, text=f"{home_team} vs {away_team} - {home_score}:{away_score}", variable=var)
        checkbox.grid(row=i + 1, column=0, sticky='w')
        wyscout_checkboxes[wyscout_id] = var

    # Display Games data on the right
    tk.Label(frame, text="Games Data", font=('Arial', 14, 'bold')).grid(row=0, column=1, padx=10, pady=10)
    for i, game in enumerate(games_data):
        home_team = game['home_team']
        away_team = game['away_team']
        home_score = game['home_score']
        away_score = game['away_score']

        # Create a label for each Games data game
        label = tk.Label(frame, text=f"{home_team} vs {away_team} - {home_score}:{away_score}")
        label.grid(row=i + 1, column=1, sticky='w')

# Load data
wyscout_directory = 'games_wyscout'
games_directory = 'games'
wyscout_files = [f for f in os.listdir(wyscout_directory) if f.endswith('.json')]
games_data = load_games_data(games_directory)

# Create GUI
root = tk.Tk()
root.title('Game Selector')
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

current_file_index = 0
wyscout_checkboxes = {}
wyscout_data = []  # Initialize wyscout_data

def on_next():
    global current_file_index, wyscout_data  # Declare wyscout_data as global
    selected_games = []
    for wyscout_id, var in wyscout_checkboxes.items():
        if var.get():
            selected_games.append(wyscout_id)

    if selected_games:
        with open('results.txt', 'a') as results_file:
            for wyscout_id in selected_games:
                game = next((g for g in wyscout_data if g['wyId'] == wyscout_id), None)
                if game:
                    results_file.write(f"{wyscout_id}, {game['home_team']}, {game['away_team']}, {game['home_score']}:{game['away_score']}\n")

    current_file_index += 1
    if current_file_index < len(wyscout_files):
        display_games(wyscout_files[current_file_index])
    else:
        messagebox.showinfo("Finished", "All files processed!")
        root.quit()

next_button = tk.Button(root, text='Next', command=on_next)
next_button.pack(pady=10)

# Start with the first file
display_games(wyscout_files[current_file_index])

root.mainloop()
