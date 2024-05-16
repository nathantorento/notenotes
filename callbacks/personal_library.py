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
            Input({'type': 'search-check', 'index': ALL}, 'value'),
            Input({'type': 'library-check', 'index': ALL}, 'value'),
            Input({'type': 'submit-link', 'index': ALL, 'resource': ALL}, 'n_clicks'),
        ],
        [
            State({'type': 'search-check', 'index': ALL}, 'id'),
            State({'type': 'library-check', 'index': ALL}, 'id'),
            State("input-link", "value"),
            State('user-library-store', 'data')
        ]
    )
    def update_personal_library(search_values,
                                library_values,
                                submit_link_clicks,
                                search_ids,
                                library_ids,
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
        
        # Add or remove songs to library when checkbox is checked or unchecked, respectively
        if 'check' in triggered_id:
            if 'search-check' in triggered_id:
                values = search_values
                ids = search_ids
            elif 'library-check' in triggered_id:
                values = library_values
                ids = library_ids
            for check, id_info in zip(values, ids):
                track_id = id_info['index']
                if check:
                    if track_id not in personal_library:
                        song_data = sample_database[sample_database['track_id'] == track_id].iloc[0]
                        personal_library[track_id] = {
                            'image': song_data['image'],
                            'title': song_data['title'],
                            'artist': song_data['artist'],
                            'album': song_data['album'],
                            'tempo': song_data['tempo'],
                            'genre': song_data['genre'],
                            'lyrics': "",
                            'lead_sheet': "",
                            'sheet_music': "",
                        }
                    return personal_library
            else:  # Removing song from library
                personal_library.pop(track_id, None)
        return personal_library
