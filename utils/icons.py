"""
icons.py

Centralizes shared icon definitions for the Dash application. These icons are imported and used across various modules to ensure consistency.

Defines:
    - edit_icon: HTML image component for the edit icon.
"""

from dash import html

edit_icon = html.Img(src="assets/edit_icon.png", style={'width': '20px'})