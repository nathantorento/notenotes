
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import time

def register_metronome_callbacks(app):

    @app.callback(
        Output("tempo-display", "children"),
        Output("tap-times", "data"),
        Input("tap-button", "n_clicks"),
        State("tap-times", "data")
    )
    def calculate_tempo(n_clicks, tap_times):
        if n_clicks == 0:
            return "Tap to set tempo", []
        
        # Capture the current time in seconds
        current_time = time.time()
        
        # Append the current time to the list of tap times
        tap_times.append(current_time)
        
        # Calculate the intervals between successive taps and the average tempo
        if len(tap_times) > 1:
            intervals = [tap_times[i] - tap_times[i-1] for i in range(1, len(tap_times))]
            average_interval = sum(intervals) / len(intervals)
            tempo = 60 / average_interval  # Convert interval to beats per minute (BPM)
            return f"Tempo: {int(tempo)} BPM", tap_times
        return "Keep tapping", tap_times
