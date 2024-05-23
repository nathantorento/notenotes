"""
home_page.py

Defines the home page content for the Dash application.

Functions:
    - get_home_page_content(): Returns the content of the home page.
"""

from dash import html
import dash_bootstrap_components as dbc

def load_homepage():
    return dbc.Container([
        dbc.Row(html.H1("Welcome to NoteNotes!", className="text-center mb-4")),
        dbc.Row(html.P(
            "Curate and manage your personal music library all in one place",
            className="text-lead text-center mb-4"
        )),
        dbc.Row(html.Div(style={'height': '2px', 'width': '80%', 'background-color': '#E3EBF1', 'margin': '20px 0px 20px 0px'}), className="my-3", justify="center"),
        dbc.Row([
            dbc.Col(html.Div([
                html.H4("Search Songs"),
                html.P("Find songs by titles, artists, or albums"),
            ]), width=4),
            dbc.Col(html.Div([
                html.H4("Personal Library"),
                html.P("Save your favorite songs and manage your setlists"),
            ]), width=4),
            dbc.Col(html.Div([
                html.H4("Song Details"),
                html.P("Store, retrieve, and automate lyrics and sheet music"),
            ]), width=4),
        ]),
        dbc.Row([
            dbc.Col(dbc.Button("Start Exploring", href="/search", color="primary", className="mt-4"), className="text-center")
        ]),
    ], fluid=True, className="py-3")
