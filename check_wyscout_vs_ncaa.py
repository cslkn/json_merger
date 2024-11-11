import os
import json

# Define directories
games_dir = 'games'
games_wyscout_dir = 'games_wyscout'
results_file = 'results.txt'

# Clear results file if it exists
if os.path.exists(results_file):
    os.remove(results_file)

# Function to format the date from YYYYMMDD to MM/DD/YYYY
def format_date(date_str):
    return f"{date_str[4:6]}/{date_str[6:8]}/{date_str[0:4]}"

# Loop through each file in the games_wyscout directory
for wyscout_file in os.listdir(games_wyscout_dir):
    if wyscout_file.endswith('.json'):
        # Extract the date from the file name (assuming the format is YYYYMMDD)
        date_str = wyscout_file[:-5]  # Remove '.json'
        formatted_date = format_date(date_str)  # Format the date

        # Load the games_wyscout JSON file
        with open(os.path.join(games_wyscout_dir, wyscout_file), 'r') as f:
            wyscout_data = json.load(f)

        # Prepare a set of (home_team, away_team) tuples from the wyscout data
        wyscout_games = {(game['home_team'], game['away_team']) for game in wyscout_data}

        # Load the corresponding games JSON file
        games_file = os.path.join(games_dir, wyscout_file)
        if os.path.exists(games_file):
            with open(games_file, 'r') as f:
                games_data = json.load(f)

            # Prepare a set of (home_team, away_team) tuples from the games data
            games = {(game['home_team'], game['away_team']) for game in games_data}
        else:
            games = set()  # If the games file does not exist, set is empty

        # Check for games that are in wyscout but not in games
        missing_games = wyscout_games - games

        # Write missing wyIds, team names, scores, and date to the results file
        with open(results_file, 'a') as result_f:
            for game in wyscout_data:
                game_tuple = (game['home_team'], game['away_team'])
                if game_tuple in missing_games:
                    result_f.write(f"Date: {formatted_date}, wyId: {game['wyId']}, Home Team: {game['home_team']}, Away Team: {game['away_team']}, Score: {game['home_score']} - {game['away_score']}\n")
