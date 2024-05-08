from dash import html, dcc, callback, Dash, Input, Output, State, callback_context, dash_table
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
    dcc.Store(id='user-library-store'),  # Add this line
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

# Initialize global dictionary to store user's song selections
user_library = {}
track_index = '2o1pb13quMReXZqE7jWsgq'
song_data = sample_database[sample_database['track_id'] == track_index].iloc[0]
user_library[track_index] = {
    'title': song_data['title'],
    'artist': song_data['artist'],
    'album': song_data['album'],
    'tempo': song_data['tempo']
}

# Callback to manage navigation and page content display
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
            html.Div(id="songs-output"),
        ])

# Callback to populate and update the library page
@app.callback(Output('library-content', 'children'), [Input('url', 'pathname')])
def update_library_view(pathname):
    if pathname == '/library':
        return [
            dbc.Row(
                [
                    dbc.Col(html.Div(f"{info['title']} by {info['artist']}"), width=10),
                    dbc.Col(dbc.Checkbox(id={'type': 'library-item', 'index': track_id}, value=True, className='library-checkbox'), width=2)
                ],
                className='library-row',
                style={'margin': '5px', 'border': '1px solid #ccc', 'padding': '10px'}
            ) for track_id, info in user_library.items()
        ]
    return []  # Return an empty list when not on the library page

# Callback to return the search results according to the search_rank function
@app.callback(
    Output('songs-output', 'children'),
    Input('search-button', 'n_clicks'),
    State('artist-input', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, value):
    if n_clicks is None or not value:
        raise PreventUpdate
    search_results = search_rank(value, sample_database)
    return [
        dbc.Row(
            [
                dbc.Col(html.Div(f"{result['title']} by {result['artist']}"), width=10),
                dbc.Col(dbc.Checkbox(id={'type': 'song-select', 'index': result['track_id']}, value=False), width=2)
            ],
            id={'type': 'song-row', 'index': result['track_id']},
            key=result['track_id'],
            className='song-row',
            style={'margin': '5px', 'border': '1px solid #ccc', 'padding': '10px', 'cursor': 'pointer'}
        ) for result in search_results
    ]

# Callback to allow the tracking of checkbox selections and manage the user library state
@app.callback(
    Output({'type': 'song-select', 'index': dash.dependencies.ALL}, 'value'),
    Input({'type': 'song-row', 'index': dash.dependencies.ALL}, 'n_clicks'),
    [State({'type': 'song-select', 'index': dash.dependencies.ALL}, 'value'),
     State({'type': 'song-row', 'index': dash.dependencies.ALL}, 'key')],
    prevent_initial_call=True
)
def toggle_song_selection(n_clicks, is_checked, track_ids):
    ctx = callback_context
    triggered_id, prop = ctx.triggered[0]['prop_id'].split('.')
    track_index = json.loads(triggered_id)['index']
    idx = track_ids.index(track_index)

    if is_checked[idx]:  # Checkbox was checked before click, so uncheck and remove from library
        user_library.pop(track_index, None)
        is_checked[idx] = False  # Explicitly setting unchecked state
    else:  # Checkbox was unchecked before click, so check and add to library
        song_data = sample_database[sample_database['track_id'] == track_index].iloc[0]
        user_library[track_index] = {
            'title': song_data['title'],
            'artist': song_data['artist'],
            'album': song_data['album'],
            'tempo': song_data['tempo']
        }
        is_checked[idx] = True  # Explicitly setting checked state

    # Return updated checkbox states to reflect the changes
    return is_checked

if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
