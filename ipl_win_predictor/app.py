import tkinter as tk
from datetime import datetime
from pipeline import run_pipeline

REFRESH_INTERVAL_MS = 15000

class IPLPredictorDesktop(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IPL Live Win Predictor")
        self.configure(bg="#f4f7fb")
        self.geometry("1040x900")
        self.resizable(False, False)

        self.running = False
        self.job = None
        self.history = []

        self._build_ui()
        self.start()  # Auto start fetching

    def _build_ui(self):
        self.columnconfigure(0, weight=1)

        top_frame = tk.Frame(self, bg="#ffffff", bd=0)
        top_frame.pack(fill="x", padx=14, pady=12)

        title_frame = tk.Frame(top_frame, bg="#ffffff")
        title_frame.pack(side="left", fill="x", expand=True)

        title_label = tk.Label(
            title_frame,
            text="IPL Live Win Predictor",
            font=("Segoe UI", 18, "bold"),
            bg="#ffffff",
            fg="#1f2d3d"
        )
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            title_frame,
            text="Live match data, smart prediction, and instant insights.",
            font=("Segoe UI", 12),
            bg="#ffffff",
            fg="#5f6c7d"
        )
        subtitle_label.pack(anchor="w", pady=(4, 0))

        button_frame = tk.Frame(top_frame, bg="#ffffff")
        button_frame.pack(side="right")

        self.start_button = tk.Button(
            button_frame,
            text="Start",
            command=self.start,
            bg="#2d6ef7",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=12,
            bd=0,
            activebackground="#1e56d1",
            activeforeground="white"
        )
        self.start_button.pack(side="left", padx=(0, 10), pady=4)

        self.stop_button = tk.Button(
            button_frame,
            text="Stop",
            command=self.stop,
            bg="#f44336",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=10,
            bd=0,
            activebackground="#d32f2f",
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=(0, 10), pady=4)

        self.refresh_button = tk.Button(
            button_frame,
            text="Refresh",
            command=self._refresh_now,
            bg="#20c997",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=10,
            bd=0,
            activebackground="#17a589"
        )
        self.refresh_button.pack(side="left", pady=4)

        self.status_label = tk.Label(
            self,
            text="Press Start to fetch live IPL data.",
            font=("Segoe UI", 12),
            bg="#e9f2ff",
            fg="#1d4b85",
            anchor="w",
            padx=16,
            pady=12,
            relief="groove"
        )
        self.status_label.pack(fill="x", padx=14, pady=(0, 10))

        body_frame = tk.Frame(self, bg="#f4f7fb")
        body_frame.pack(fill="both", expand=True, padx=14, pady=(0, 10))
        body_frame.columnconfigure(0, weight=1)
        body_frame.columnconfigure(1, weight=1)
        body_frame.rowconfigure(0, weight=1)

        left_panel = tk.Frame(body_frame, bg="#f4f7fb")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 7))
        right_panel = tk.Frame(body_frame, bg="#f4f7fb")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(7, 0))

        self.match_card = tk.Frame(left_panel, bg="#2d6ef7", bd=0, relief="flat")
        self.match_card.pack(fill="x", pady=(0, 10))

        self.match_title = tk.Label(
            self.match_card,
            text="No match loaded",
            font=("Segoe UI", 16, "bold"),
            bg="#2d6ef7",
            fg="white",
            pady=12,
            padx=16,
            wraplength=920,
            justify="center",
            anchor="center"
        )
        self.match_title.pack(fill="x")

        self.score_label = tk.Label(
            self.match_card,
            text="",
            font=("Segoe UI", 14),
            bg="#1e55c7",
            fg="white",
            pady=10,
            padx=16
        )
        self.score_label.pack(fill="x")

        self.prob_frame = tk.Frame(left_panel, bg="#ffffff", bd=0)
        self.prob_frame.pack(fill="x", pady=(0, 10))

        prob_label = tk.Label(
            self.prob_frame,
            text="Win Probability",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg="#1f2d3d",
            anchor="w"
        )
        prob_label.pack(fill="x", padx=14, pady=(10, 4))

        self.prob_canvas = tk.Canvas(
            self.prob_frame,
            height=32,
            bg="#edf2fa",
            bd=0,
            highlightthickness=0
        )
        self.prob_canvas.pack(fill="x", padx=14, pady=(0, 12))

        self.prob_text = tk.Label(
            self.prob_frame,
            text="Team 1 50.00% | Team 2 50.00%",
            font=("Segoe UI", 12),
            bg="#ffffff",
            fg="#5f6c7d"
        )
        self.prob_text.pack(fill="x", padx=14, pady=(0, 12))

        self.stats_frame = tk.Frame(left_panel, bg="#ffffff", bd=0)
        self.stats_frame.pack(fill="x", pady=(0, 10))

        stats_title = tk.Label(
            self.stats_frame,
            text="Match Statistics",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg="#1f2d3d",
            anchor="w"
        )
        stats_title.pack(fill="x", padx=14, pady=(10, 6))

        self.stats_vars = {}
        stats = [
            ("Total Runs", "runs"),
            ("Wickets", "wickets"),
            ("Overs", "overs"),
            ("Run Rate", "run_rate")
        ]
        for label_text, key in stats:
            row = tk.Frame(self.stats_frame, bg="#ffffff")
            row.pack(fill="x", padx=14, pady=6)
            label = tk.Label(
                row,
                text=label_text,
                font=("Segoe UI", 12),
                bg="#ffffff",
                fg="#5f6c7d"
            )
            label.pack(side="left")
            value = tk.Label(
                row,
                text="0",
                font=("Segoe UI", 12, "bold"),
                bg="#ffffff",
                fg="#334155"
            )
            value.pack(side="right")
            self.stats_vars[key] = value

        self.details_frame = tk.Frame(left_panel, bg="#ffffff", bd=0)
        self.details_frame.pack(fill="both", expand=True)

        details_title = tk.Label(
            self.details_frame,
            text="Live Match Details",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg="#1f2d3d",
            anchor="w"
        )
        details_title.pack(fill="x", padx=14, pady=(10, 6))

        self.details_text = tk.Text(
            self.details_frame,
            height=16,
            bg="#f8fafe",
            fg="#1f2d3d",
            bd=0,
            wrap="word",
            font=("Segoe UI", 11),
            padx=12,
            pady=12
        )
        self.details_text.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.details_text.configure(state="disabled")

        self.scorecard_frame = tk.Frame(right_panel, bg="#ffffff", bd=0)
        self.scorecard_frame.pack(fill="both", expand=True)

        scorecard_title = tk.Label(
            self.scorecard_frame,
            text="Scorecard",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg="#1f2d3d",
            anchor="w"
        )
        scorecard_title.pack(fill="x", padx=14, pady=(10, 6))

        self.scorecard_text = tk.Text(
            self.scorecard_frame,
            bg="#f8fafe",
            fg="#1f2d3d",
            bd=0,
            wrap="none",
            font=("Segoe UI", 11),
            padx=12,
            pady=12
        )
        self.scorecard_text.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.scorecard_text.configure(state="disabled")

        self.history_label = tk.Label(
            self,
            text="Prediction history will appear after start.",
            font=("Segoe UI", 11),
            bg="#f4f7fb",
            fg="#475569",
            anchor="w",
            padx=16,
            pady=10
        )
        self.history_label.pack(fill="x", padx=14, pady=(0, 10))

    def start(self):
        if self.running:
            return
        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="Fetching live IPL data...", fg="#0b6623")
        self._fetch_data()

    def stop(self):
        if not self.running:
            return
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Prediction stopped.", fg="#b45309")
        if self.job is not None:
            self.after_cancel(self.job)
            self.job = None

    def _refresh_now(self):
        if self.running:
            self._fetch_data()
        else:
            self.status_label.config(text="Start the prediction first to refresh.", fg="#b45309")

    def _draw_probability_bar(self, team1_value, team2_value):
        self.prob_canvas.delete("all")
        width = self.prob_canvas.winfo_width() or 900
        team1_width = int(width * (team1_value / 100))
        self.prob_canvas.create_rectangle(0, 0, team1_width, 32, fill="#2d6ef7", width=0)
        self.prob_canvas.create_rectangle(team1_width, 0, width, 32, fill="#f64b5d", width=0)

    def _fetch_data(self):
        result = run_pipeline()
        if "error" in result:
            self.status_label.config(text=f"Error: {result['error']}", fg="#b45309")
            self.stop()
            return
        self._update_ui(result)
        self.history.append((datetime.now().strftime("%H:%M:%S"), result["batting_win"], result["bowling_win"], result.get("prediction_available", True)))
        latest = self.history[-1]
        if latest[3]:
            history_text = f"History: {len(self.history)} updates. Latest {latest[0]} — {result['team1']} {latest[1]}% | {result['team2']} {latest[2]}%"
        else:
            history_text = f"History: {len(self.history)} updates. Latest {latest[0]} — prediction unavailable until chase starts."
        self.history_label.config(text=history_text)
        if self.running:
            self.status_label.config(text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}", fg="#1f2d3d")
            self.job = self.after(REFRESH_INTERVAL_MS, self._fetch_data)

    def _update_ui(self, data):
        team1 = data["team1"]
        team2 = data["team2"]
        self.match_title.config(text=f"{team1} vs {team2}")
        self.score_label.config(text=f"Current Score: {data['score']}")
        if data.get("prediction_available", True):
            self.prob_text.config(text=f"{team1} {data['batting_win']}%  |  {team2} {data['bowling_win']}%")
            self._draw_probability_bar(data['batting_win'], data['bowling_win'])
        else:
            self.prob_text.config(text="Prediction unavailable until second innings chase")
            self._draw_probability_bar(50, 50)
        self.stats_vars["runs"].config(text=str(data["runs"]))
        self.stats_vars["wickets"].config(text=str(data["wickets"]))
        self.stats_vars["overs"].config(text=f"{data['overs']:.1f}")
        self.stats_vars["run_rate"].config(text=f"{data['run_rate']:.2f}")

        details_lines = []
        if data.get("match_status"):
            details_lines.append(f"Match Status: {data['match_status']}")
        batting_team = data.get("batting_team")
        bowling_team = data.get("bowling_team")
        if batting_team:
            details_lines.append(f"Batting Team: {batting_team}")
        if bowling_team:
            details_lines.append(f"Bowling Team: {bowling_team}")
        details_lines.append(f"Current Score: {data['score']}")
        details_lines.append(f"Run Rate: {data['run_rate']:.2f}")
        if data.get("target", 0) > 0:
            details_lines.append(f"Target: {data['target']}")
        if not data.get("prediction_available", True):
            details_lines.append("")
            details_lines.append("Note: Prediction is available only after the second innings chase begins.")
        details_lines.append("")

        batsmen = data.get("batsmen", [])
        if batsmen:
            details_lines.append("Current Batsmen:")
            for batsman in batsmen:
                role = " (striker)" if batsman.get("is_striker") else ""
                details_lines.append(
                    f"• {batsman['name']}{role} — {batsman['runs']} ({batsman['balls']}) | 4s:{batsman['fours']} 6s:{batsman['sixes']} SR:{batsman['strike_rate']}"
                )
            details_lines.append("")

        bowler = data.get("bowler", {})
        if bowler:
            details_lines.append("Current Bowler:")
            details_lines.append(
                f"• {bowler.get('name','Unknown')} — Overs:{bowler.get('overs',0)}, Runs:{bowler.get('runs',0)}, Wkts:{bowler.get('wickets',0)}, Econ:{bowler.get('economy',0)}"
            )
            details_lines.append("")

        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", "end")
        self.details_text.insert("end", "\n".join(details_lines))
        self.details_text.configure(state="disabled")

        self.scorecard_text.configure(state="normal")
        self.scorecard_text.delete("1.0", "end")
        scorecard = data.get("scorecard", [])
        if scorecard:
            lines = ["Name                Runs Balls 4s 6s  SR   Out"]
            lines.append("-" * 74)
            for row in scorecard:
                lines.append(
                    f"{row['name'][:18]:18} {row['runs']:>4} {row['balls']:>5} {row['fours']:>2} {row['sixes']:>2} {row['strike_rate']:>5}  {row.get('out_desc','Not Out')}"
                )
            self.scorecard_text.insert("end", "\n".join(lines))
        else:
            summary = [
                "Live scorecard details are not provided by the current feed.",
                "This section now shows the available summary information below:",
                "",
                f"Match Status: {data.get('match_status', 'Unknown')}",
                f"Current Score: {data.get('score', 'N/A')}",
                f"Batting Team: {data.get('batting_team', 'N/A')}",
                f"Bowling Team: {data.get('bowling_team', 'N/A')}",
            ]
            if data.get('target', 0):
                summary.append(f"Target: {data['target']}")
            self.scorecard_text.insert("end", "\n".join(summary))
        self.scorecard_text.configure(state="disabled")

if __name__ == "__main__":
    app = IPLPredictorDesktop()
    app.mainloop()
