"""
app.py

This module initializes the Dash application instance with required configurations.
It imports necessary libraries and sets up the external stylesheets and suppresses callback exceptions.
"""

from dash import Dash
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)
