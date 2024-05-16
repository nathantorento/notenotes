"""
styles.py

Centralizes shared style definitions for the Dash application. These styles are imported and used across various modules to ensure consistency.

Defines:
    - main_header_style: Style for main headers.
    - border_style, icon_style, nav_bar_style, menu_col_style, main_display_style, track_display_style: Other shared styles.
"""

# border_style = '0px solid #ccc'
banner_style = {
    'display': 'flex',
    'justify-content': 'center',  # Center horizontally
    'align-items': 'center',  # Center vertically
    'width': '100%',
    'padding': '10px 0 20px 0',
}
icon_style = {'height': '20px', 'margin-right': '10px'}
nav_bar_style = {'display': 'flex', 'alignItems': 'center'}
menu_col_style = {
    'maxWidth': '200px',
    'background': 'linear-gradient(to top, #C0DDF3, #ffffff)',
    'height': '100vh',
    'padding': '10px 0px 10px 0px',
    'display': 'flex',
    'flexDirection': 'column',
}
main_header_style = {
    'fontSize': '32px',
    'padding': '0px 0px 10px 0px'
}
main_display_style = {
    'background': 'linear-gradient(to top, #DAE9F4, #ffffff)',
    'height': '100vh',
    'padding': '20px 20px 20px 20px',
    'overflow-y': 'auto',
}
track_display_style = {
    'border': '1px solid #ccc',
    'border-radius': '10px',
    'margin': '0px',
    'padding': '10px',
    'cursor': 'pointer',
    'display': 'flex',
    'flexWrap': 'nowrap',
}
