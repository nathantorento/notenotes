"""
callbacks/search_page.py

Defines callback functions related to the search page in the Dash application.

Functions:
    - register_search_page_callbacks(app): Registers callbacks related to the search page.
"""

from dash import html, dcc, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from app import app
from utils.helpers import song_row_generator, search_rank
from utils.styles import main_header_style, track_display_style
import pandas as pd

# Load the pre-processed data
sample_database = pd.read_csv('data/sample_database.csv')


def register_search_page_callbacks(app):

    @app.callback(
        Output('search-output', 'children'),
        [
            Input('search-button', 'n_clicks'),
            Input('user-library-store', 'data')
        ],
        State('search-input', 'value'),
        prevent_initial_call=True
    )
    def output_search(n_clicks, library_data, value):
        if n_clicks is None or not value:
            raise PreventUpdate

        search_results = search_rank(value, sample_database)

        return [
            dbc.Row(
                song_row_generator(
                    result['track_id'], result, "search", library_data),
                key=result['track_id'],
                className='search-row',
                style=track_display_style
            ) for result in search_results
        ]
