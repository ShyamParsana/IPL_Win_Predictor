import requests
import json
import os

headers = {
    "X-RapidAPI-Key": os.getenv("CRICBUZZ_API_KEY", "5c33620a9amsh70ae137a1c51a44p1e617bjsn4010c4348464"),
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

res = requests.get("https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live", headers=headers, timeout=15)
data = res.json()

print("Total typeMatches:", len(data.get("typeMatches", [])))

for idx, type_match in enumerate(data.get("typeMatches", [])):
    print(f"\n[{idx}] matchType: {type_match.get('matchType')}")
    
    if type_match.get("matchType") == "League":
        print("  ✓ Found League type")
        for s_idx, series_match in enumerate(type_match.get("seriesMatches", [])):
            series_name = series_match.get("seriesAdWrapper", {}).get("seriesName")
            print(f"    [{s_idx}] Series: {series_name}")
            
            matches = series_match.get("seriesAdWrapper", {}).get("matches", [])
            print(f"        Total matches: {len(matches)}")
            
            for m_idx, match in enumerate(matches):
                info = match.get("matchInfo", {})
                series_in_match = info.get("seriesName", "")
                status = info.get("status", "")
                team1 = info.get("team1", {}).get("teamName", "")
                team2 = info.get("team2", {}).get("teamName", "")
                
                print(f"        [{m_idx}] {team1} vs {team2}")
                print(f"             Series: {series_in_match}")
                print(f"             Status: {status}")
                print(f"             Has 'IPL': {'IPL' in series_in_match.upper()}")
