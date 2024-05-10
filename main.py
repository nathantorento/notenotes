from requests import post, get
from dash import html, dcc, callback, Dash, Input, Output, State, callback_context, dash_table, no_update
from dash.exceptions import PreventUpdate
from dash.dependencies import ClientsideFunction
import dash
import dash_bootstrap_components as dbc
import pandas as pd

# Initialize the Dash app with Bootstrap CSS
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Define the modal which will be triggered to open by clicking on a song row
modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Song Details"), close_button=True),
        dbc.ModalBody([
            dbc.Button("Genre: None", className="mr-1", style={'background-color': 'white', 'color': 'black'}),
            dbc.Button("Tempo: 130 BPM", className="mr-1", style={'background-color': 'white', 'color': 'black'}),
            dbc.Button("Add: Custom", className="mr-1", style={'background-color': 'white', 'color': 'black'}),
            html.Br(),
            html.Br(),
            dbc.Button("Add: Lyrics", className="mr-1", style={'background-color': 'white', 'color': 'black'}),
            dbc.Button("Add: Lead Sheet", className="mr-1", style={'background-color': 'white', 'color': 'black'}),
            dbc.Button("Add: Sheet Music", className="mr-1", style={'background-color': 'white', 'color': 'black'}),
        ], style={'backgroundColor': '#B0E0E6'}),
    ],
    id="modal-song-details",
    is_open=False,  # Initially don't show the modal
    centered=True,
    backdrop="static"  # Dismiss by clicking outside of modal
)

# Unified style guides
border_style = '0px solid #ccc'
icon_style = {'height': '20px', 'margin-right': '10px'}
nav_bar_style = {'display': 'flex', 'alignItems': 'center'}
menu_col_style = {
    'maxWidth': '200px',
    'backgroundColor': '#C0DDF3', 
    'height': '100vh', 
    'padding': '10px 0px 10px 0px',
    'display': 'flex',
    'flexDirection': 'column',
}
main_header_style = {
    'fontSize': '32px',
    'padding': '0 0 10px 0'
}
main_display_style = {
    'backgroundColor': '#DAE9F4', 
    'height': '100vh', 
    'padding': '10px 10px 10px 10px',
}

# Define the layout of the app
app.layout = html.Div([
    dcc.Store(id='user-library-store', storage_type='session'),
    dcc.Location(id='url', refresh=False),
    dbc.Container([
        dbc.Row([
            # Left-side Menu Bar (fixed width)
            dbc.Col([
                # Banner with Logo and Wordmark
                html.Div(
                    html.Img(src="assets/notenotes_banner.png", style={'width': '80%', 'height': 'auto'}),
                    style={
                        'display': 'flex',
                        'justify-content': 'center',  # Center horizontally
                        'align-items': 'center',  # Center vertically
                        'width': '100%',
                        'padding': '10px 0 20px 0',
                    }
                ),
                # Top nav section
                dbc.Nav([
                    # Search Nav Bar with Icon
                    dbc.NavLink(
                        html.Div([
                            html.Img(src="/assets/search_icon.png", style=icon_style),
                            html.Span("Search", style={'fontWeight': 'bold'})
                        ], style=nav_bar_style),
                        href="/",
                        active="exact"
                    ),

                    # Library Nav Bar with Icon
                    dbc.NavLink(
                        html.Div([
                            html.Img(src="/assets/library_icon.png", style=icon_style),
                            html.Span("Library", style={'fontWeight': 'bold'})
                        ], style=nav_bar_style),
                        href="/library",
                        active="exact"
                    ),
                ], vertical=True, pills=True, style={'width': '100%'}),

                # Push top nav bar up and bottom nav bar down with "FlexGrow" Div
                html.Div(style={'flexGrow': 1}), # This div pushes the following content to the bottom

                # Bottom nav section
                dbc.Nav([
                    # User Nav Bar
                    dbc.NavLink(
                        html.Div([
                            html.Img(src="/assets/user_icon.png", style=icon_style),
                            html.Span("User", style={'fontWeight': 'bold'})
                        ], style=nav_bar_style),
                        href="/user",
                        active="exact"
                    ),
                ], vertical=True, pills=True, style={'width': '100%'}),
            ], style=menu_col_style), # menu column style

            # Right-side main page
            dbc.Col([

            ], id='page-content', style=main_display_style),
        ], style={'height': '100vh', 'margin': '0'}),
    ], fluid=True, style={'height': '100vh', 'padding': '0'}),
    html.Div(id='dummy-div', style={'display': 'none'}),
], style={'margin': '0', 'height': '100vh'})

# Return tracks by a specified priority
def search_rank(keyword, df):
    search_results = []
    keyword = keyword.lower()

    # Search for matching titles
    title_matches = df[df['title'].str.lower().str.contains(keyword)]
    search_results.extend(title_matches['track_id'].tolist())

    # Search for matching albums
    album_matches = df[df['album'].str.lower().str.contains(keyword)]
    for track_id in album_matches['track_id']:
        if track_id not in search_results:
            search_results.append(track_id)

    # Search for matching artists
    artist_matches = df[df['artist'].str.lower().str.contains(keyword)]
    for track_id in artist_matches['track_id']:
        if track_id not in search_results:
            search_results.append(track_id)

    # Create a list of search results in the format "Title – Artist"
    search_results = df[df['track_id'].isin(search_results)]
    return search_results.to_dict('records')

# Load the pre-processed data
sample_database = pd.read_csv('sample_database.csv')

# Row style
row_style = {'margin': '5px', 'border': '1px solid #ccc', 'border-radius': '20px', 'padding': '10px', 'cursor': 'pointer'}

# Display /Search or /Library page, content determined by later callbacks
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/library':
        return html.Div([
            html.H1('Library', style=main_header_style),
            html.Div(id='library-content')
        ])
    else:  # Default will handle the search page
        return html.Div([
            dcc.Input(id="artist-input", type="text", placeholder="Enter song/artist/album", debounce=True),
            html.Button("Search", id="search-button"),
            html.Div(id="songs-output")
        ])

# Display /library page by reading from user-library-store
@app.callback(
    Output('library-content', 'children'),
    Input('user-library-store', 'data')
)
def display_library(data):
    if not data:
        return "Your library is empty. Why don't you add some songs?"
    return [
        dbc.Row(
            [
                dbc.Col(html.Div(f"{info['title']} by {info['artist']}", id={'type': 'library-row', 'index': track_id}, n_clicks=0, style={'cursor': 'pointer'}), width=10),
                dbc.Col(dbc.Checkbox(
                    id={'type': 'library-item', 'index': track_id}, 
                    value=True), 
                width=2)
            ],
            key=track_id,
            className='library-row',
            style=row_style
        ) for track_id, info in data.items()
    ]

# Return the search results according to the search_rank function
@app.callback(
    Output('songs-output', 'children'),
    Input('search-button', 'n_clicks'),
    State('artist-input', 'value'),
    State('user-library-store', 'data'),  # Add this to get current library state
    prevent_initial_call=True
)
def output_search(n_clicks, value, library_data):
    if n_clicks is None or not value:
        raise PreventUpdate

    search_results = search_rank(value, sample_database)
    return [
        dbc.Row(
            [
                dbc.Col(html.Div(f"{result['title']} by {result['artist']}", id={'type': 'song-row', 'index': result['track_id']}, n_clicks=0, style={'cursor': 'pointer'}), width=10),
                dbc.Col(dbc.Checkbox(
                    id={'type': 'song-select', 'index': result['track_id']},
                    value=(result['track_id'] in library_data) if library_data else False
                ), width=2)
            ],
            key=result['track_id'],
            className='song-row',
            style=row_style
        ) for result in search_results
    ]

# Display and update library when songs are checked/unchecked in either search results or library view.
@app.callback(
    Output('user-library-store', 'data'),
    [Input({'type': 'song-select', 'index': dash.dependencies.ALL}, 'value'),
     Input({'type': 'library-item', 'index': dash.dependencies.ALL}, 'value')],
    [State({'type': 'song-select', 'index': dash.dependencies.ALL}, 'id'),
     State({'type': 'library-item', 'index': dash.dependencies.ALL}, 'id'),
     State('user-library-store', 'data')]
)
def update_user_library(search_values, library_values, search_ids, library_ids, current_data):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_data  # Return the current state if no inputs have triggered the callback
    
    triggered_input = ctx.triggered[0]['prop_id']

    # Check which input triggered the callback
    if 'song-select' in triggered_input:
        # Logic for handling search results checkboxes
        for check, id_info in zip(search_values, search_ids):
            track_id = id_info['index']
            if check:
                song_data = sample_database[sample_database['track_id'] == track_id].iloc[0]
                current_data[track_id] = {
                    'title': song_data['title'],
                    'artist': song_data['artist'],
                    'album': song_data['album'],
                    'tempo': song_data['tempo']
                }
            else:
                current_data.pop(track_id, None)
    elif 'library-item' in triggered_input:
        # Logic for handling library checkboxes
        for is_checked, item_id in zip(library_values, library_ids):
            track_id = item_id['index']
            if not is_checked:
                current_data.pop(track_id, None)

    return current_data

# Toggle the modal visibility when any song row is clicked in search or library.
@app.callback(
    Output("modal-song-details", "is_open"),
    [Input({'type': 'song-row', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [State("modal-song-details", "is_open")]
)
def toggle_modal(n_clicks_list, is_open):
    if any(n_clicks for n_clicks in n_clicks_list if n_clicks):
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
