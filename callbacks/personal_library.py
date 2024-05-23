"""
callbacks/personal_library.py

Defines callback functions related to managing the personal library in the Dash application.

Functions:
    - register_personal_library_callbacks(app): Registers callbacks related to personal library management.
"""

from dash import callback_context, no_update
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import ast
from app import app

# Load the pre-processed data
sample_database = pd.read_csv('data/sample_database.csv')


def register_personal_library_callbacks(app):

    @app.callback(
        Output('user-library-store', 'data'),
        [
            Input({'type': 'song-check', 'index': ALL}, 'n_clicks'),
            Input({'type': 'submit-link', 'index': ALL, 'resource': ALL}, 'n_clicks'),
        ],
        [
            State("input-link", "value"),
            State('user-library-store', 'data')
        ]
    )
    def update_personal_library(song_clicks, 
                                submit_link_clicks,
                                input_link,
                                personal_library):
        # Determine which actions were performed
        ctx = callback_context
        if not ctx.triggered:
            return personal_library

        triggered_id = ctx.triggered[0]['prop_id']
        dict_result = ast.literal_eval(triggered_id.split('.')[0]) # Use ast.literal_eval to safely evaluate the string to a dictionary
        track_id = dict_result['index']
        
        # Add input link to the correct resource
        if any(click > 0 for click in submit_link_clicks):
            resource_type = dict_result['resource']
            personal_library[track_id][resource_type] = input_link
            return personal_library
        
        # Add or remove songs to library when add_icon is clicked
        # if any(click > 0 for click in search_n_clicks + library_n_clicks):
        if any(click > 0 for click in song_clicks):
            if track_id not in personal_library:
                song_data = sample_database[sample_database['track_id'] == track_id].iloc[0]
                personal_library[track_id] = {
                    'image': song_data['image'],
                    'title': song_data['title'],
                    'artist': song_data['artist'],
                    'album': song_data['album'],
                    'tempo': song_data['tempo'],
                    'genre': song_data['genre'],
                    'lyrics': '',
                    'lead_sheet': '',
                    'sheet_music': '',
                }
                return personal_library
            else:  # If check is unchecked, remove song from library
                    personal_library.pop(track_id, None)
        return personal_library
