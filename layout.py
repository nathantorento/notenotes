"""
layout.py

Defines the layout of the Dash application. Imports and uses various components 
and styles to build the structure of the app.

Imports:
    - html, dcc from dash: For creating Dash HTML and core components.
    - dbc from dash_bootstrap_components: For using Bootstrap components in Dash.
    - input_modal, info_modal from components: Modularized components.
    - menu_col_style, main_display_style, icon_style, nav_bar_style from styles: Shared styles.
    - edit_icon from icons: Shared icon element.

Defines:
    - layout: The layout structure of the Dash application.
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.input_modal_components import input_modal
from components.info_modal_components import info_modal
from components.user_components import user_dropdown
from utils.styles import banner_style, menu_col_style, main_display_style, icon_style, nav_bar_style

# Define the layout of the app
layout = html.Div([
    dcc.Store(id='user-library-store', storage_type='session', data={}),
    dcc.Location(id='url', refresh=False),
    dbc.Container([
        dbc.Row([
            # Left-side Menu Bar (fixed width)
            dbc.Col([
                # Banner with Logo and Wordmark
                html.Div(
                    html.Img(src="assets/notenotes_banner.png",
                             style={'width': '80%', 'height': 'auto'}),
                    style=banner_style
                ),
                # Top nav section
                dbc.Nav([
                    # Search Nav Bar with Icon
                    dbc.NavLink(
                        html.Div([
                            html.Img(src="/assets/search_icon.png",
                                     style=icon_style),
                            html.Span("Search", style={'fontWeight': 'bold'})
                        ], style=nav_bar_style),
                        href="/search",
                        active="exact",
                        className="nav-link-custom"
                    ),

                    # Library Nav Bar with Icon
                    dbc.NavLink(
                        html.Div([
                            html.Img(src="/assets/library_icon.png",
                                     style=icon_style),
                            html.Span("Library", style={'fontWeight': 'bold'})
                        ], style=nav_bar_style),
                        href="/library",
                        active="exact",
                        className="nav-link-custom"
                    ),
                ], className="custom-nav", vertical=True, pills=True, style={'width': '100%'}),

                # Push top nav bar up and bottom nav bar down with "FlexGrow" Div
                # This div pushes the following content to the bottom
                html.Div(style={'flexGrow': 1}),

                # Bottom nav section
                dbc.Nav([
                    # User Nav Bar
                    dbc.NavLink(
                        html.Div([
                            html.Img(src="/assets/user_icon.png",
                                     style={'height': '30px',
                                            'margin-right': '10px'}
                                     ),
                            html.Span("User", style={'fontWeight': 'bold'}),
                            html.Div(style={'flexGrow': 1}),
                            user_dropdown
                        ], style=nav_bar_style),
                        href="/user",
                        active="exact",
                        className="nav-link-custom"
                    ),
                ], className="custom-nav", vertical=True, pills=True, style={'width': '100%'}),
            ], style=menu_col_style),  # menu column style

            # Right-side main page
            dbc.Col([

            ], id='page-content', style=main_display_style),
        ], style={'height': '100vh', 'margin': '0'}),
    ], fluid=True, style={'height': '100vh', 'padding': '0'}),
    info_modal,
    input_modal,
    html.Div(id='dummy-div', style={'display': 'none'}),
], style={'margin': '0', 'height': '100vh'})
