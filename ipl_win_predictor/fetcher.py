import requests
import os

def fetch_live_data():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

    headers = {
        "X-RapidAPI-Key": os.getenv("CRICBUZZ_API_KEY", "5c33620a9amsh70ae137a1c51a44p1e617bjsn4010c4348464"),
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }
    
    try:
        print("Fetching live match data from Cricbuzz API...")
        res = requests.get(url, headers=headers, timeout=15)

        if res.status_code == 403:
            print("API key expired")
            print("Get a new API key from: https://rapidapi.com/cricketapilive/api/cricbuzz-cricket")
            print("Update the API key in environment variable CRICBUZZ_API_KEY")
            return {"error": "API_KEY_EXPIRED", "message": "Your Cricbuzz API key has expired. Please get a new key from RapidAPI."}

        res.raise_for_status()
        data = res.json()

        # Check if we have live matches
        if not data or "typeMatches" not in data or not data["typeMatches"]:
            print("No live matches currently available")
            return None

        # Find IPL matches specifically
        ipl_match = None
        for type_match in data["typeMatches"]:
            if type_match.get("matchType") == "League":
                for series_match in type_match.get("seriesMatches", []):
                    for match in series_match.get("seriesAdWrapper", {}).get("matches", []):
                        series_name = match.get("matchInfo", {}).get("seriesName", "").upper()
                        # Check for Indian Premier League, IPL, or just PREMIER LEAGUE
                        if "INDIAN PREMIER" in series_name or "IPL" in series_name:
                            ipl_match = match
                            break
                    if ipl_match:
                        break
                if ipl_match:
                    break

        if not ipl_match:
            print("No IPL matches currently live")
            return None

        match_data = ipl_match
        print("Found live IPL match")

        info = match_data["matchInfo"]
        score = match_data["matchScore"]
        print(f"Full score: {score}")

        team1 = info.get("team1", {}).get("teamName", "Team 1")
        team2 = info.get("team2", {}).get("teamName", "Team 2")
        curr_bat_id = info.get("currBatTeamId")
        match_status = info.get("status", info.get("matchStatus", "Live match"))

        # Check if match has started
        if "team1Score" not in score and "team2Score" not in score:
            print("Match hasn't started yet")
            return None

        batting_team = None
        bowling_team = None
        innings = None

        if curr_bat_id:
            if curr_bat_id == info.get("team1", {}).get("teamId"):
                batting_team = team1
                bowling_team = team2
                innings = score.get("team1Score", {}).get("inngs1") or score.get("team2Score", {}).get("inngs1")
            elif curr_bat_id == info.get("team2", {}).get("teamId"):
                batting_team = team2
                bowling_team = team1
                innings = score.get("team2Score", {}).get("inngs1") or score.get("team1Score", {}).get("inngs1")

        if innings is None:
            if "team2Score" in score:
                batting_team = team2
                bowling_team = team1
                innings = score["team2Score"]["inngs1"]
            else:
                batting_team = team1
                bowling_team = team2
                innings = score["team1Score"]["inngs1"]

        print(f"Current innings data: {innings}")

        runs = innings["runs"]
        wickets = innings["wickets"]
        overs = float(innings["overs"])

        score_text = f"{runs}/{wickets} ({overs} ov)"

        target = innings.get("target", 0)

        # --- Extract Batsmen Information ---
        batsmen = []
        bowler_info = {}
        scorecard = []
        players_list = {"team1": [], "team2": []}

        # Note: Detailed batsman/bowler data not available in live API summary
        # Fetching scorecard not supported for live matches

        # Players list from info
        if "players" in info:
            if "team1" in info["players"]:
                players_list["team1"] = [p.get("name", "Unknown") for p in info["players"]["team1"]]
            if "team2" in info["players"]:
                players_list["team2"] = [p.get("name", "Unknown") for p in info["players"]["team2"]]

        return {
            "team1": team1,
            "team2": team2,
            "batting_team": batting_team,
            "bowling_team": bowling_team,
            "score": score_text,
            "runs": runs,
            "wickets": wickets,
            "overs": overs,
            "target": target,
            "batsmen": batsmen,
            "bowler": bowler_info,
            "scorecard": scorecard,
            "run_rate": round(runs / (overs + 0.01), 2) if overs > 0 else 0,
            "match_status": match_status
        }

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None