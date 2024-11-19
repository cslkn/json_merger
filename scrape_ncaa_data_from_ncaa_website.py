import requests
import os
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Generate valid list of dates given start and end date
def generate_date_range(start_date, end_date):
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)
    return date_list

# Date ranges for NCAA seasons (also contains season division IDs for NCAA url handling)
date_ranges = [
    ("08/09/2023", "12/11/2023", "18180"),
    ("08/11/2022", "12/12/2022", "17906"),
    ("08/12/2021", "12/12/2021", "17700")
]

# Generate date ranges
dates_with_seasons = []
for start, end, season_division in date_ranges:
    start_date = datetime.strptime(start, "%m/%d/%Y")
    end_date = datetime.strptime(end, "%m/%d/%Y")
    dates_with_seasons.extend([(date, season_division) for date in generate_date_range(start_date, end_date)])

folder_name = "games_ncaa"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

all_games = []

# Loop through each date in range
for date, season_division in dates_with_seasons:
    date_str = date.strftime("%m/%d/%Y")
    url = f"https://stats.ncaa.org/season_divisions/{season_division}/livestream_scoreboards?utf8=%E2%9C%93&season_division_id=&game_date={date_str}&conference_id=0&tournament_id=&commit=Submit"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    # HTML fetch
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        
        # Parse HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find relevant table rows
        games = []
        rows = soup.find_all('tr', id=lambda x: x and x.startswith('contest_'))

        # Loop through rows two at a time (home and away)
        for i in range(0, len(rows), 2):
            home_row = rows[i]
            away_row = rows[i + 1] if (i + 1) < len(rows) else None # Check for away team row if applicable

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

            # Create game entry
            game = {
                "date": date.strftime('%Y-%m-%d'),
                "home_team": home_team,
                "away_team": away_team,
                "home_score": home_score,
                "away_score": away_score
            }
            games.append(game)

        # Add the games to all_games list
        all_games.extend(games)
        print(f"Retrieved {len(games)} games for {date.strftime('%Y-%m-%d')}")

    else:
        print(f"Failed to retrieve the page for {date.strftime('%Y-%m-%d')}. Status code: {response.status_code}")

combined_filename = os.path.join(folder_name, "all_games_2021-2023.json")

with open(combined_filename, "w", encoding="utf-8") as file:
    json.dump(all_games, file, indent=4)

print(f"All game data saved to {combined_filename}")
