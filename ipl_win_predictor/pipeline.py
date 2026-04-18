from fetcher import fetch_live_data
from features import create_features
from model import predict

def run_pipeline():
    data = fetch_live_data()

    if data is None:
        return {"error": "No live match found"}

    if isinstance(data, dict) and "error" in data:
        if data["error"] == "API_KEY_EXPIRED":
            return {"error": data["message"]}
        return {"error": "API Error"}

    features = create_features(data)
    prediction_available = features is not None
    if prediction_available:
        pred = predict(features)
        batting_win = pred["batting_team_win"]
        bowling_win = pred["bowling_team_win"]
    else:
        batting_win = 50.0
        bowling_win = 50.0

    return {
        "team1": data["team1"],
        "team2": data["team2"],
        "score": data["score"],
        "batting_win": batting_win,
        "bowling_win": bowling_win,
        "prediction_available": prediction_available,
        "batsmen": data.get("batsmen", []),
        "bowler": data.get("bowler", {}),
        "scorecard": data.get("scorecard", []),
        "run_rate": data.get("run_rate", 0),
        "runs": data.get("runs", 0),
        "wickets": data.get("wickets", 0),
        "overs": data.get("overs", 0),
        "target": data.get("target", 0)
    }