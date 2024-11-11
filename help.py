import os
import json

# Path to the directory containing your JSON files
directory = 'games'
teams = set()

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):  # Check for JSON files
        file_path = os.path.join(directory, filename)
        
        with open(file_path, 'r') as file:
            try:
                games = json.load(file)  # Load the JSON content
                for game in games:
                    teams.add(game['home_team'])  # Add home team
                    teams.add(game['away_team'])  # Add away team
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")

# Write the unique team names to a text file
with open('ncaa_teams.txt', 'w') as output_file:
    for team in sorted(teams):
        output_file.write(f"{team}\n")

print("Team names have been written to wyscout_teams.txt.")
