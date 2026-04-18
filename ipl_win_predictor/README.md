# IPL Live Win Predictor

A Python desktop application (Tkinter GUI) that predicts the winner of IPL (Indian Premier League) cricket matches in real-time using machine learning. Fetches live match data from Cricbuzz API and displays probability analysis with player stats and scorecard.

## Features

✅ **Real-time Live Data**: Fetch live IPL match data from Cricbuzz Cricket API  
✅ **AI Predictions**: Random Forest ML model predicts win probability  
✅ **Visual Dashboard**: Modern Tkinter desktop UI with probability bar graph  
✅ **Match Stats**: Current runs, wickets, overs, run rate display  
✅ **Player Info**: Current batsmen, bowler, and team player lists  
✅ **Scorecard**: Live match scorecard with all batsmen stats  
✅ **Auto-Refresh**: Updates predictions every 15 seconds  
✅ **History Tracking**: Maintains prediction history across updates  

## Tech Stack

- **Frontend**: Tkinter (Python GUI)
- **Backend**: Python 3.8+
- **ML**: Scikit-learn (Random Forest Classifier)
- **API**: Cricbuzz Cricket API (RapidAPI)
- **Data**: Pandas, NumPy

## Project Structure

```
ipl_win_predictor/
├── app.py                 # Main Tkinter desktop application
├── pipeline.py            # Data orchestration pipeline
├── model.py               # ML model loading & prediction
├── features.py            # Feature engineering
├── fetcher.py             # Cricbuzz API integration
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── models/
    └── win_model.pkl      # Trained Random Forest model
```

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ipl_win_predictor.git
cd ipl_win_predictor
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Get Cricbuzz API Key
--> Already put in this project.
To use live data, you need a Cricbuzz API key:

1. Go to [Cricbuzz Cricket API on RapidAPI](https://rapidapi.com/cricketapilive/api/cricbuzz-cricket)
2. Sign up for free (or login)
3. Subscribe to the "Basic" plan (free tier available)
4. Copy your API key
5. Open `fetcher.py` and replace the API key on line 7:

```python
headers = {
    "X-RapidAPI-Key": "YOUR_API_KEY_HERE",  # Replace with your key
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}
```

## Running the Application

### Start the Desktop App
```bash
python app.py
```

The application window will open with:
- **Title Bar**: "IPL Live Win Predictor"
- **Buttons**: Start | Stop | Refresh
- **Left Panel**: Match card, win probabilities, stats, and live details
- **Right Panel**: Live scorecard with player stats

### Using the Application

1. **Click "Start"** → Fetches live IPL match data
2. **Auto-Refresh** → Updates every 15 seconds automatically
3. **Click "Refresh"** → Manual data update
4. **Click "Stop"** → Stops fetching and predictions
5. **View Results** → See win probabilities, player stats, and predictions history

## How It Works

### Data Flow
```
Cricbuzz API
    ↓
fetch_live_data() [fetcher.py]
    ↓
Extract: team names, score, batsmen, bowlers
    ↓
create_features() [features.py]
    ↓
Runs | Wickets | Balls Left | Required Run Rate
    ↓
predict() [model.py]
    ↓
Random Forest Model → Win Probability (%)
    ↓
Display in Tkinter GUI [app.py]
```

### Feature Engineering
- **Runs**: Current match runs
- **Wickets**: Wickets fallen
- **Balls Left**: Remaining balls in 20 overs
- **Required Run Rate**: Runs needed per over

## API Response

The app fetches live match data including:
- Team names and current scores
- Current batsmen (striker & non-striker)
- Current bowler and bowling stats
- Full scorecard with all batsmen
- List of team players

## Requirements

- Python 3.8 or higher
- Windows, macOS, or Linux
- Internet connection (for live data)
- Cricbuzz API key (free)

## Dependencies

See `requirements.txt`:
```
pandas>=1.5.0
scikit-learn>=1.3.0
joblib>=1.3.0
requests>=2.31.0
```

## Model Details

- **Algorithm**: Random Forest Classifier
- **Trees**: 100 estimators
- **Features**: 4 (runs, wickets, balls_left, required_rr)
- **Output**: Win probability for both teams (0-100%)
- **Training Data**: IPL historical match data

## Troubleshooting

### API Key Error (403 Forbidden)
**Problem**: "You are not subscribed to this API"  
**Solution**: 
1. Check that your API key is valid
2. Verify you subscribed to the Cricbuzz API on RapidAPI
3. Ensure the key is pasted correctly in `fetcher.py`

### No Live Matches Found
**Problem**: "No IPL matches currently live"  
**Solution**:
- Check if IPL season is active
- Verify internet connection
- Ensure Cricbuzz API is working

### Tkinter Not Found
**Problem**: `ModuleNotFoundError: No module named 'tkinter'`  
**Solution**:
- **Windows**: Tkinter is included with Python
- **macOS**: `brew install python-tk3.x` (replace x with version)
- **Linux**: `sudo apt-get install python3-tk`

## Future Enhancements

- [ ] Add multi-match monitoring
- [ ] Dark mode UI theme
- [ ] Export predictions to CSV
- [ ] Historical win rate analysis
- [ ] Player performance stats
- [ ] Mobile app version

## License

This project is open source and available under the MIT License.

## Disclaimer

This application is for educational purposes. Predictions are based on ML model analysis and should not be used for betting or gambling.

## Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## Support

For issues or questions, open a GitHub issue or contact the author.

---

**Author**: Your Name  
**Last Updated**: April 2026  
**Status**: Active Development ✅
