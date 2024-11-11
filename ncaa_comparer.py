import json
import os

# Define the directories
games_directory = 'games'
match_info_directory = 'match_info_no_events'
output_directory = 'combined_match_data'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Function to load game data
def load_games_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Function to load match info data
def load_match_info(match_id):
    match_filename = f"{match_info_directory}/{match_id}.json"
    if os.path.exists(match_filename):
        with open(match_filename, 'r') as file:
            return json.load(file)
    return None

# Function to convert score to int with error handling
def safe_convert_score(score):
    if score == 'N/A':
        return None  # or you can return 0 or any other default value you prefer
    try:
        return int(score)
    except ValueError:
        return None  # Handle any other conversion issues

# Function to combine data
def combine_data(games_data):
    combined_data = []
    for game in games_data:
        # Extract team names and scores
        home_team = game['home_team']
        away_team = game['away_team']
        home_score = safe_convert_score(game['home_score'])
        away_score = safe_convert_score(game['away_score'])

        # If scores are not valid, skip this game
        if home_score is None or away_score is None:
            print(f"Skipping game due to invalid scores: {game}")
            continue

        # Construct match ID from teams and scores
        match_id = f"{home_team.replace(' ', '_')}-{away_team.replace(' ', '_')}_{home_score}-{away_score}"

        # Load match info
        match_info = load_match_info(match_id)

        if match_info:
            # Combine the game and match info
            combined_entry = {
                "game": game,
                "match_info": match_info
            }
            combined_data.append(combined_entry)

    return combined_data

# Function to save combined data
def save_combined_data(data, date_str):
    output_filename = f"{output_directory}/combined_data_{date_str}.json"
    with open(output_filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)

# Main processing
def main():
    # Loop through each JSON file in the games directory
    for filename in os.listdir(games_directory):
        if filename.endswith('.json'):
            date_str = filename.split('.')[0]  # Extract date from filename
            games_data = load_games_data(os.path.join(games_directory, filename))

            # Combine data for the current date
            combined_data = combine_data(games_data)

            # Save combined data to output directory
            save_combined_data(combined_data, date_str)

            # Print combined data for debugging
            print(f"Combined data for {date_str}:")
            print(json.dumps(combined_data, indent=4))

if __name__ == "__main__":
    main()
