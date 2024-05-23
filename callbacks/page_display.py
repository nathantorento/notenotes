"""
callbacks/page_display.py

Defines the callback function to display the appropriate page content based on the URL pathname in the Dash application.

Functions:
    - register_page_display_callbacks(app): Registers the callback for displaying the appropriate page content.
"""

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html, no_update
from app import app
from utils.styles import main_header_style
from callbacks.home_page import load_homepage

def register_page_display_callbacks(app):

    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
    )
    def display_page(pathname):
        if pathname == '/':
            return html.Div([
                html.H1('Home', style=main_header_style),
                load_homepage()  # Use the function to get home page content
            ])
        elif pathname == '/library':
            return html.Div([
                html.H1('Library', style=main_header_style),
                html.Div(id='library-content')
            ])
        elif pathname == '/search':
            return html.Div([
                html.H1("Search", style=main_header_style),
                html.Div([
                    dbc.Input(
                        id="search-input",
                        type="text",
                        placeholder="Search for any song, artist, album",
                        debounce=True,
                        style={
                            'flexGrow': 1,
                            'marginRight': '10px',  # space between input and search button
                        }
                    ),
                    html.Button("Search", id="search-button",
                                style={'height': '38px', 'borderRadius': '10px', 'borderColor': '#ccc'})
                ], style={
                    'display': 'flex',
                    'flexWrap': 'nowrap',
                    'padding': '10px 0px 10px 0px',
                }),
                html.Div(id="search-output")
            ])
        else:
            return no_update  # Handle other paths if necessary
