from dash import html, dcc, callback, Dash, Input, Output, State, callback_context, dash_table, no_update
import dash
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from requests import post, get
import json
import pandas as pd

# Initialize the Dash app with Bootstrap CSS
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Define the layout of the app
app.layout = html.Div([
    dcc.Store(id='user-library-store', storage_type='session'),
    dcc.Location(id='url', refresh=False),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("NoteNotes", className="display-4", style={'fontSize': '24px', 'text-align': 'center'}),
                html.Hr(),
                dbc.Nav([
                    dbc.NavLink("Search", href="/", active="exact"),
                    dbc.NavLink("Library", href="/library", active="exact"),
                ], vertical=True, pills=True),
                html.Hr(),
                dbc.Nav([
                    dbc.NavLink("User", href="#", active="exact"),
                    html.Div(className="bi bi-person-circle")
                ], vertical=True, pills=True),
            ], width=2, style={'backgroundColor': '#ADD8E6', 'height': '100vh'}),
            dbc.Col(id='page-content'),
        ]),
    ]),
    html.Div(id='dummy-div', style={'display': 'none'})  # Hidden div for any unused callback outputs
], style={'margin': '10px'})

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
            html.H1('Your Song Library'),
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
        dbc.Row([
            dbc.Col(html.Div(f"{info['title']} by {info['artist']}"), width=10),
            dbc.Col(dbc.Checkbox(id={'type': 'library-item', 'index': track_id}, value=True), width=2)
        ],
        style = row_style
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
                dbc.Col(html.Div(f"{result['title']} by {result['artist']}"), width=10),
                dbc.Col(dbc.Checkbox(
                    id={'type': 'song-select', 'index': result['track_id']},
                    value=(result['track_id'] in library_data) if library_data else False  # Check if the song is in the library
                ), width=2)
            ],
            id={'type': 'song-row', 'index': result['track_id']},
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

if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
