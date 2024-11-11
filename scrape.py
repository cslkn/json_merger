import requests
import os
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Function to generate a list of dates
def generate_date_range(start_date, end_date):
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)
    return date_list

# Define the start and end dates
start_date = datetime.strptime("08/09/2023", "%m/%d/%Y")
end_date = datetime.strptime("12/11/2023", "%m/%d/%Y")

# Generate the date range
dates = generate_date_range(start_date, end_date)

# Create the 'games_ncaa' folder if it doesn't exist
folder_name = "games_ncaa"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Initialize a list to hold all game data
all_games = []

# Loop through each date in the range
for date in dates:
    date_str = date.strftime("%m/%d/%Y")
    url = f"https://stats.ncaa.org/season_divisions/18180/livestream_scoreboards?utf8=%E2%9C%93&season_division_id=&game_date={date_str}&conference_id=0&tournament_id=&commit=Submit"

    # Headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    # Fetching the HTML content
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
        
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the relevant table rows
        games = []
        rows = soup.find_all('tr', id=lambda x: x and x.startswith('contest_'))

        # Loop through rows two at a time (home and away)
        for i in range(0, len(rows), 2):
            home_row = rows[i]
            away_row = rows[i + 1] if (i + 1) < len(rows) else None  # Check for the next row

            # Extract home team data
            home_team = home_row.find('td', valign='middle').find('img')['alt'] if home_row.find('td', valign='middle').find('img') else "Unknown Home Team"
            home_score = home_row.find('div', class_='p-1').text.strip() if home_row.find('div', class_='p-1') else "N/A"

            # Extract away team data
            if away_row:
                away_team = away_row.find('td', valign='middle').find('img')['alt'] if away_row.find('td', valign='middle').find('img') else "Unknown Away Team"
                away_score = away_row.find('div', class_='p-1').text.strip() if away_row.find('div', class_='p-1') else "N/A"
            else:
                away_team = "Unknown Away Team"
                away_score = "N/A"

            # Create a game entry
            game = {
                "date": date.strftime('%Y-%m-%d'),
                "home_team": home_team,
                "away_team": away_team,
                "home_score": home_score,
                "away_score": away_score
            }
            games.append(game)

        # Add the games to the all_games list
        all_games.extend(games)

    else:
        print(f"Failed to retrieve the page for {date.strftime('%Y-%m-%d')}. Status code: {response.status_code}")

# Define the filename for the combined JSON file
combined_filename = os.path.join(folder_name, "all_games.json")

# Save the combined JSON content to a file
with open(combined_filename, "w", encoding="utf-8") as file:
    json.dump(all_games, file, indent=4)

print(f"All game data saved to {combined_filename}")
