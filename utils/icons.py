"""
icons.py

Centralizes shared icon definitions for the Dash application. These icons are imported and used across various modules to ensure consistency.

Defines:
    - edit_icon: HTML image component for the edit icon.
"""

from dash import html
icon_size = '30px'
edit_icon = html.Img(src="/assets/edit_icon.png", style={'width': icon_size})
lyrics_icon = html.Img(src="/assets/lyrics_icon.png", style={'width': icon_size})
lead_sheet_icon = html.Img(src="/assets/lead_sheet_icon.png", style={'width': icon_size})
sheet_music_icon = html.Img(src="/assets/sheet_music_icon.png", style={'width': icon_size})