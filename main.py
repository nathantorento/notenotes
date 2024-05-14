# Import all relevant packages
from requests import post, get
from dash import html, dcc, callback, Dash, Input, Output, State, callback_context, dash_table, no_update
from dash.exceptions import PreventUpdate
from dash.dependencies import ClientsideFunction, ALL
import json
import ast
import dash
import dash_bootstrap_components as dbc
import pandas as pd

# Initialize the Dash app with Bootstrap CSS
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

# Unified style guides
border_style = '0px solid #ccc'
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
    'overflow-y': 'auto',  # Enables vertical scrolling
}
track_display_style = {
    'border': '1px solid #ccc',
    'border-radius': '10px',
    'margin': '0px',
    'padding': '10px',
    'cursor': 'pointer',
    'display': 'flex',
    'flexWrap': 'nowrap',
    # 'padding': '10px 0px 10px 0px',
}

# Define the modal which will be triggered to open by clicking on a song row
modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle(
            "Song Attributes/Resources"), close_button=True),
        dbc.ModalBody([
            html.Div(id="modal-attributes"),
            # space in between attributes and resources
            html.Div(style={"height": "20px"}),
            html.Div(id="modal-resources")
        ]),
    ],
    id="modal-status",
    is_open=False,  # Initially don't show the modal
    centered=True,
    backdrop=True  # Dismiss by clicking outside of modal
)

# Modal attributes content
def modal_attributes_generator(song_data):
    # Function to generate buttons in a custom, reusable format
    def button_generator(song_data, attribute):
        value = song_data.get(attribute, 'None')
        if attribute == "tempo" and value != 'None':
            # Convert to float, round up, and append units
            value = f"{round(value)}bpm"
        else:
            value = f"{value}"

        button = dbc.Button(f"{attribute.title()}: {value}", style={
            'background-color': 'white',
            'color': 'black',
            'width': '150px'})
        return button

    genre = button_generator(song_data, "genre")
    tempo = button_generator(song_data, "tempo")

    attributes = html.Div([genre, tempo], style={
        'display': 'flex',
        'justify-content': 'space-between'})

    return attributes

# Modal resources content (dynamic based on whether the song is in the user's library)
def modal_resources_generator(song_data):
    # Function to generate resource buttons in a custom, reusable format
    def resource_button_generator(resource_name, link):
        return dbc.Button(resource_name, href=song_data.get(link, '#'), target="_blank", className="mr-1", style={
            'background-color': 'white',
            'color': 'black',
            'width': '150px'})

    lyrics = resource_button_generator("Lyrics", 'lyrics_link')
    lead_sheet = resource_button_generator("Lead Sheet", 'lead_sheet_link')
    sheet_music = resource_button_generator("Sheet Music", 'sheet_music_link')

    resources = html.Div([lyrics, lead_sheet, sheet_music], style={
        'display': 'flex',
        'justify-content': 'space-between'})

    return resources

# Define contents of "User" dropdown menu
user_dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Settings", href="/settings"),
        dbc.DropdownMenuItem("Logout", href="/logout"),
    ],
    nav=True,
    in_navbar=True,
)

# Define the layout of the app
app.layout = html.Div([
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
    modal,
    html.Div(id='dummy-div', style={'display': 'none'}),
], style={'margin': '0', 'height': '100vh'})

# Load the pre-processed data
sample_database = pd.read_csv('sample_database.csv')

# Row generator
def song_row_generator(track_id, info, page, personal_library=None):
    row_type = f"{page}-row"
    check_type = f"{page}-check"

    # Rows of tracks
    row = dbc.Col(html.Div(
        f"{info['title']} by {info['artist']}",
        id={'type': row_type, 'index': track_id},
        n_clicks=0,
        style={'cursor': 'pointer'}
    ), width=7)

    # Accompanying checkmarks per row
    if page == "search":  # check marks for search results
        checkbox = dbc.Col(dbc.Checkbox(
            id={'type': 'search-check', 'index': info['track_id']},
            value=(info['track_id']
                   in personal_library) if personal_library else False
        ), width=2)

    elif page == "library":  # check marks auto checked in library
        checkbox = dbc.Col(dbc.Checkbox(
            id={'type': check_type, 'index': track_id},
            value=True
        ), width=2)

    edit = dbc.Col(html.Img(src="assets/edit_icon.png",
                   style={'height': '20px'}), width=2)

    return row, checkbox, edit

# Display /Search or /Library page, content determined by later callbacks
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/library':
        return html.Div([
            # Library Header
            html.H1('Library', style=main_header_style),
            # Library contents
            html.Div(id='library-content')
        ])
    elif pathname == '/search':  # Default will handle the search page
        return html.Div(
            [
                # Search Header
                html.H1("Search", style=main_header_style),

                # Search bar
                html.Div([
                    dbc.Input(
                        id="search-input",
                        type="text",
                        placeholder="Search for any song, artist, album",
                        debounce=True,
                        style={
                            'flexGrow': 1,
                            'marginRight': '10px',  # space between input and search button
                        }
                    ),
                    # match search bar's height
                    html.Button("Search", id="search-button",
                                style={'height': '38px', 'borderRadius': '10px', 'borderColor': '#ccc'})
                ], style={
                    'display': 'flex',
                    'flexWrap': 'nowrap',
                    'padding': '10px 0px 10px 0px',
                }),

                # Search bar outputs
                html.Div(id="search-output")
            ])

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

# Return the search results according to the search_rank function
@app.callback(
    Output('search-output', 'children'),
    Input('search-button', 'n_clicks'),
    State('search-input', 'value'),
    # Add this to get current library state
    State('user-library-store', 'data'),
    prevent_initial_call=True
)
def output_search(n_clicks, value, data):
    if n_clicks is None or not value:
        raise PreventUpdate

    search_results = search_rank(value, sample_database)

    return [
        dbc.Row(
            [
                song_row_generator(
                    result['track_id'], result, "search", data)[0],
                song_row_generator(
                    result['track_id'], result, "search", data)[1]
            ],
            key=result['track_id'],
            className='search-row',
            style=track_display_style
        ) for result in search_results
    ]

# Load user-library-store contents for /Library
@app.callback(
    Output('library-content', 'children'),
    Input('user-library-store', 'data')
)
def load_library(data):
    if not data:
        return "Your library is empty. Why don't you add some songs?"
    else:
        return [
            dbc.Row(
                [
                    song_row_generator(track_id, info, "library")[0],  # row
                    song_row_generator(track_id, info, "library")[
                        1],  # checkbox
                    song_row_generator(track_id, info, "library")[2],  # edit
                ],
                key=track_id,
                className='library-row',
                style=track_display_style
            ) for track_id, info in data.items()
        ]

# This callback will toggle the modal open state based on multiple triggers.
@app.callback(
    [
        Output("modal-status", "is_open"),
        Output('modal-attributes', 'children'),
        Output('modal-resources', 'children')
    ],
    [
        Input({'type': 'search-row', 'index': ALL}, 'n_clicks'),
        Input({'type': 'library-row', 'index': ALL}, 'n_clicks'),
    ],
    [
        State("modal-status", "is_open"),
        State('user-library-store', 'data')
    ],
    prevent_initial_call=True
)
def toggle_update_modal(search_row_clicks, library_row_clicks, is_open, personal_library):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open, no_update, no_update  # Ensure to return a tuple with three items

    triggered_element = ctx.triggered[0]['prop_id']
    index = ast.literal_eval(triggered_element.split('.')[0])['index']

    # Retrieve song data, checking personal library first
    song_data = personal_library.get(index) or sample_database[sample_database['track_id'] == index].drop(columns='track_id').iloc[0].to_dict()

    # Modal content generation based on the song data and whether it is in the library
    if any(click > 0 for click in search_row_clicks + library_row_clicks):
        if song_data:
            modal_attributes = modal_attributes_generator(song_data)
            modal_resources = modal_resources_generator(song_data) if index in personal_library else []
            return not is_open, modal_attributes, modal_resources
        else:
            return not is_open, [], []
    return is_open, no_update, no_update

# Display song details like genre and tempo and, if the song is in the library, provide options to add or edit links for lyrics, lead sheets, and full sheet music
@app.callback(
    Output('user-library-store', 'data'),
    [Input({'type': 'search-check', 'index': ALL}, 'value'),
     Input({'type': 'library-check', 'index': ALL}, 'value'),
     Input({'type': 'add-lyrics', 'index': ALL}, 'n_clicks'),
     Input({'type': 'edit-lyrics', 'index': ALL}, 'n_clicks'),
     Input({'type': 'add-lead', 'index': ALL}, 'n_clicks'),
     Input({'type': 'edit-lead', 'index': ALL}, 'n_clicks'),
     Input({'type': 'add-sheet', 'index': ALL}, 'n_clicks'),
     Input({'type': 'edit-sheet', 'index': ALL}, 'n_clicks')],
    [State({'type': 'search-check', 'index': ALL}, 'id'),
     State({'type': 'library-check', 'index': ALL}, 'id'),
     State('user-library-store', 'data')]
)
def manage_personal_library(search_values, library_values, add_lyrics_clicks, edit_lyrics_clicks,
                            add_lead_clicks, edit_lead_clicks, add_sheet_clicks, edit_sheet_clicks,
                            search_ids, library_ids, current_data):
    # Determine which actions were performed
    ctx = callback_context
    if not ctx.triggered:
        return current_data

    triggered_id = ctx.triggered[0]['prop_id']
    dictionary_part = triggered_id.split('.')[0]
    # Use ast.literal_eval to safely evaluate the string to a dictionary
    dict_result = ast.literal_eval(dictionary_part)
    index = dict_result['index']

    # Add or remove songs to library when checkbox is checked or unchecked, respectively
    if 'search-check' in triggered_id or 'library-check' in triggered_id:
        if 'search-check' in triggered_id:
            values = search_values
            ids = search_ids
        elif 'library-check' in triggered_id:
            values = library_values
            ids = library_ids
        for check, id_info in zip(values, ids):
            track_id = id_info['index']
            if check:
                song_data = sample_database[sample_database['track_id']
                                            == track_id].iloc[0]
                current_data[track_id] = {
                    'title': song_data['title'],
                    'artist': song_data['artist'],
                    'album': song_data['album'],
                    'tempo': song_data['tempo'],
                    'genre': song_data['genre']
                }
            else:  # Removing song from library
                current_data.pop(track_id, None)

    if 'add-' in triggered_id or 'edit-' in triggered_id:
        if 'lyrics' in triggered_id:
            current_data[index]['lyrics'] = link
        elif 'lead' in triggered_id:
            current_data[index]['lead_sheet'] = link
        elif 'sheet' in triggered_id:
            current_data[index]['full_sheet'] = link

    return current_data

if __name__ == '__main__':
    app.run_server(debug=True, port=3000)

