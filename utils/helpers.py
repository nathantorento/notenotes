"""
utils/helpers.py

Contains helper functions for the Dash application. These functions are used across various modules for generating components and handling data.

Defines:
    - modal_attributes_generator(song_data): Generates modal attributes for a given song data.
    - modal_resources_generator(song_data, track_id): Generates modal resources for a given song data and track ID.
    - song_row_generator(track_id, info, page, personal_library): Generates a song row component.
    - search_rank(keyword, df): Ranks search results based on the keyword and dataframe.
"""

from dash import html
import dash_bootstrap_components as dbc
from utils.icons import edit_icon, lyrics_icon, lead_sheet_icon, sheet_music_icon

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

        button = dbc.Button(
            html.Span(f"{attribute.title()}: {value}", style={'fontSize': '16px'}),
            style={
                'background-color': '#65fe08)',
                'color': 'white',
                'width': '150px'}
        )
        return button

    genre = button_generator(song_data, "genre")
    tempo = button_generator(song_data, "tempo")

    attributes = html.Div([genre, tempo], style={
        'display': 'flex',
        'justify-content': 'space-between'})

    return attributes

# Modal resources content (dynamic based on whether the song is in the user's library)


def modal_resources_generator(song_data, track_id):
    lyrics_link = song_data.get('lyrics', '')
    lead_sheet_link = song_data.get('lead_sheet', '')
    sheet_music_link = song_data.get('sheet_music', '')

    # Function to generate resource buttons in a custom, reusable format
    def resource_button_generator(resource_name, link, track_id):
        if link == '':
            button_text = f"Add: {resource_name}"
            button = dbc.Button(
                html.Span(button_text, style={'fontSize': '14px'}),
                id={
                    "index": track_id,
                    "type": "edit-resource",
                    "resource": resource_name.lower().replace(" ", "_")
                },
                n_clicks=0,
                style={'cursor': 'pointer',
                       'background-color': '#f9be82',
                       'color': 'white',
                       'width': '150px'}
            )
        else:
            button = dbc.Button(
                html.Span(resource_name, style={'fontSize': '16px'}),
                href=link,
                id={
                    "index": track_id,
                    "type": "edit-resource",
                    "resource": resource_name.lower().replace(" ", "_")
                },
                n_clicks=0,
                style={'cursor': 'pointer',
                       'background-color': '#f9be82',
                       'color': 'blue',
                       'textDecoration': 'underline',
                       'width': '150px'}
            )
        return button

    lyrics = resource_button_generator(
        "Lyrics", lyrics_link, track_id)
    lead_sheet = resource_button_generator(
        "Lead Sheet", lead_sheet_link, track_id)
    sheet_music = resource_button_generator(
        "Sheet Music", sheet_music_link, track_id)

    resources = dbc.Row(
        html.Div([lyrics, lead_sheet, sheet_music], style={
            'display': 'flex',
            'justify-content': 'space-between'}
        ), key=track_id, className='edit-resource')

    return resources

# Row generator


def song_row_generator(track_id, info, page, personal_library=None):
    row_type = f"{page}-row"
    check_type = f"{page}-check"

    image = dbc.Col(html.Img(
        src=info['image'],
        style={
            'width': '50px',
            'borderRadius': '10px',
        }
    ), width=1, style={
        'display': 'flex',
        'justify-content': 'center',  # Center horizontally
        'align-items': 'center',  # Center vertically
    })

    # Rows of tracks
    row = dbc.Col(html.Div([
        html.Div(info['title'], style={
            'fontSize': '18px',
            'color': 'black',
            'marginBottom': '5px'
        }),
        html.Div(info['artist'], style={
            'fontSize': '16px',
            'color': 'gray'
        }),
    ], id={'type': row_type, 'index': track_id}, n_clicks=0, style={'cursor': 'pointer', 'marginLeft': '10px'}), 
    width=4)

    # Accompanying checkmarks per row
    checkbox = dbc.Col(dbc.Checkbox(
        id={'type': check_type, 'index': track_id},
        value=(track_id in personal_library) if personal_library else False
    ), width=2, style={
        'display': 'flex',
        'justify-content': 'center',  # Center horizontally
        'align-items': 'center',  # Center vertically
    }
    )

    row_contents = [image, row, checkbox]

    # Add edit icon if the song is in the library
    if track_id in personal_library:
        edit = dbc.Col(html.Button(
            edit_icon,
            id={"type": "edit-icon", "index": track_id},
            n_clicks=0,
            className='resource-icon',
            style={'border': 'none', 'background': 'none', 'cursor': 'pointer', 'margin': '0'}
        ), style = {
            'display': 'flex',
            'justify-content': 'center',  # Center horizontally
            'align-items': 'center',  # Center vertically
        })
        row_contents.append(edit)

    # Add icons for resources
    extra_resources = []
    for resource_name in ['lyrics', 'lead_sheet', 'sheet_music']:
        if track_id in personal_library and personal_library[track_id][resource_name]!='':
            resource = dbc.Col(html.Button(
                globals()[f"{resource_name}_icon"],
                id={
                    "index": track_id,
                    "type": "edit-resource",
                    "resource": resource_name
                },
                n_clicks=0,
                className='resource-icon',
                style={'border': 'none', 'background': 'none', 'cursor': 'pointer', 'margin': '0'}
            ))
            extra_resources.append(resource)
        else:
            pass
    if extra_resources:
        extra_resources = dbc.Col(
            html.Div(extra_resources, style={
                'display': 'flex',
                'justify-content': 'space-between',
            }), style={
                'display': 'flex',
                'justify-content': 'center',  # Center horizontally
                'align-items': 'center',  # Center vertically
            })
        row_contents.append(extra_resources)

    return row_contents

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
