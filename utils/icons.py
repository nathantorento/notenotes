"""
icons.py

Centralizes shared icon definitions for the Dash application. These icons are imported and used across various modules to ensure consistency.

Defines:
    - edit_icon: HTML image component for the edit icon.
"""

from dash import html
icon_size = '30px'
add_icon_unfilled = html.Img(src="/assets/add_icon_unfilled.png", style={'width': icon_size})
add_icon_filled = html.Img(src="/assets/add_icon_filled.png", style={'width': icon_size})
edit_icon = html.Img(src="/assets/edit_icon.png", style={'width': icon_size})
lyrics_icon = html.Img(src="/assets/lyrics_icon.png", style={'width': icon_size})
chords_icon = html.Img(src="/assets/chords_icon.png", style={'width': icon_size})
sheet_music_icon = html.Img(src="/assets/sheet_music_icon.png", style={'width': icon_size})