import joblib
import os
import logging

logger = logging.getLogger(__name__)

model_path = os.path.join(os.path.dirname(__file__), 'models', 'win_model.pkl')

if os.path.exists(model_path):
    model = joblib.load(model_path)
    logger.info(f"✓ Model loaded from {model_path}")
else:
    model = None
    logger.warning(f"⚠ Model not found at {model_path}. Using 50/50 predictions.")

def predict(features):
    if model is None:
        return {
            "batting_team_win": 50.0,
            "bowling_team_win": 50.0
        }
    
    probs = model.predict_proba([features])[0]
    
    return {
        "batting_team_win": round(probs[1]*100, 2),
        "bowling_team_win": round(probs[0]*100, 2)
    }