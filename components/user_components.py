"""
user.py

This module defines the "User" dropdown menu component for the Dash application using Dash Bootstrap Components (dbc).

Components:
    - user_dropdown: A dropdown menu with links to "Settings" and "Logout".

Usage:
    Import this module and include the `user_dropdown` component in the layout of your Dash application where needed.

Example:
    from user import user_dropdown

    app.layout = html.Div([
        ...,
        user_dropdown,
        ...
    ])
"""

import dash_bootstrap_components as dbc

# Define contents of "User" dropdown menu
user_dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Settings", href="/settings"),
        dbc.DropdownMenuItem("Logout", href="/logout"),
    ],
    nav=True,
    in_navbar=True,
)
