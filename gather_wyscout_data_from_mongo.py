import os
import json
from datetime import datetime

'''
Pull games from locally downloaded mongo instance and put them in a single JSON file
'''

input_directory = 'match_info_no_events'
output_directory = 'games_wyscout'

os.makedirs(output_directory, exist_ok=True)

output_data = []

for filename in os.listdir(input_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(input_directory, filename)

        # Read specific JSON file
        with open(file_path, 'r') as file:
            match_info = json.load(file)

            date_str = match_info.get('dateutc')
            if date_str:
                match_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

                label = match_info.get('label')
                wy_id = match_info.get('wyId')

                # Extract home and away teams, scores
                if label:
                    teams, scores = label.rsplit(', ', 1)
                    home_team, away_team = teams.split(' - ')
                    home_score, away_score = scores.split(' - ')

                    # Create a dictionary for the match data, include wyId and match date
                    match_data = {
                        "wyId": wy_id,
                        "match_date": match_date.strftime('%Y-%m-%d %H:%M:%S'),
                        "home_team": home_team.strip(),
                        "away_team": away_team.strip(),
                        "home_score": home_score.strip(),
                        "away_score": away_score.strip()
                    }

                    # Add match data to output list
                    output_data.append(match_data)

# Write the output data to single JSON file
output_file_path = os.path.join(output_directory, 'all_games.json')

with open(output_file_path, 'w') as output_file:
    json.dump(output_data, output_file, indent=4)

print("Data has been processed and saved in 'games_wyscout/all_games.json'.")
