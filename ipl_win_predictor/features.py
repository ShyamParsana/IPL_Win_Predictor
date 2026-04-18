def create_features(data):
    if not isinstance(data, dict):
        raise ValueError("Invalid data format")
    
    runs = data.get("runs", 0)
    wickets = data.get("wickets", 0)
    overs = data.get("overs", 0)
    target = data.get("target", 0)

    # Prediction only makes sense in the second innings chase.
    if target <= 0:
        return None

    # Convert overs like 18.1 into actual ball count: 18 overs and 1 ball = 109 balls.
    overs_int = int(overs)
    balls_fraction = int(round((overs - overs_int) * 10))
    balls_bowled = overs_int * 6 + balls_fraction
    total_balls = 20 * 6
    balls_left = total_balls - balls_bowled

    if balls_left <= 0:
        return None

    req_rr = (target - runs) / (balls_left / 6 + 1e-5)

    return [runs, wickets, balls_left, req_rr]