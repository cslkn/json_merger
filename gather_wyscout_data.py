import os
import json
from datetime import datetime

# Define the directory containing the JSON files and the output directory
input_directory = 'match_info_no_events'
output_directory = 'games_wyscout'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

output_data = []

# Loop through each file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(input_directory, filename)

        # Read the JSON file
        with open(file_path, 'r') as file:
            match_info = json.load(file)

            # Extract dateutc and check if the game took place in 2023
            date_str = match_info.get('dateutc')
            if date_str:
                match_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

                # Only consider matches from 2023
                if match_date.year == 2023:
                    label = match_info.get('label')
                    wy_id = match_info.get('wyId')  # Extract the wyId field

                    # Extract home and away teams and scores from label
                    if label:
                        teams, scores = label.rsplit(', ', 1)
                        home_team, away_team = teams.split(' - ')
                        home_score, away_score = scores.split(' - ')

                        # Create a dictionary for the match data, including wyId and match date
                        match_data = {
                            "wyId": wy_id,  # Include the wyId in the output
                            "match_date": match_date.strftime('%Y-%m-%d %H:%M:%S'),  # Include the match date
                            "home_team": home_team.strip(),
                            "away_team": away_team.strip(),
                            "home_score": home_score.strip(),
                            "away_score": away_score.strip()
                        }

                        # Add the match data to the output list
                        output_data.append(match_data)

# Write the output data to a single JSON file in the output directory
output_file_path = os.path.join(output_directory, 'all_games_2023.json')

with open(output_file_path, 'w') as output_file:
    json.dump(output_data, output_file, indent=4)

print("Data has been processed and saved in 'games_wyscout/all_games_2023.json'.")
