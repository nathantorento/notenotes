"""
callbacks/library_page.py

Defines callback functions related to the library page in the Dash application.

Functions:
    - register_library_page_callbacks(app): Registers callbacks related to the library page.
"""

from dash.dependencies import Input, Output
from dash import html, no_update
import dash_bootstrap_components as dbc
from app import app
from utils.helpers import song_row_generator
from utils.styles import main_header_style, track_display_style


def register_library_page_callbacks(app):

    @app.callback(
        Output('library-content', 'children'),
        Input('user-library-store', 'data')
    )
    def load_library(data):
        if not data:
            return "Your library is empty. Why don't you add some songs?"
        else:
            return [
                dbc.Row(
                    song_row_generator(track_id, info, "library", data),
                    key=track_id,
                    className='library-row',
                    style=track_display_style
                ) for track_id, info in data.items()
            ]
