"""
utils/helpers.py

Contains helper functions for the Dash application. These functions are used across various modules for generating components and handling data.

Defines:
    - modal_attributes_generator(song_data): Generates modal attributes for a given song data.
    - modal_resources_generator(song_data, track_id): Generates modal resources for a given song data and track ID.
    - song_row_generator(track_id, info, page, personal_library): Generates a song row component.
    - search_rank(keyword, df): Ranks search results based on the keyword and dataframe.
"""

import re
from dash import html
import dash_bootstrap_components as dbc
from utils.icons import add_icon_unfilled, add_icon_filled, edit_icon, lyrics_icon, chords_icon, sheet_music_icon

def modal_attributes_generator(song_data):
    # List of attributes to exclude from button generation
    excluded_attributes = ['image', 'title', 'artist', 'album', 'lyrics', 'chords', 'sheet_music']

    # Function to generate buttons in a custom, reusable format
    def button_generator(attribute, value):
        if attribute == "tempo" and value != 'None':
            # Convert to float, round up, and append units
            value = f"{round(float(value))}bpm"
        return dbc.Button(
            html.Span(f"{attribute.title()}: {value}", style={'fontSize': '16px'}),
            style={
                'background-color': '#95CDF6',
                'border': 'none',
                'color': 'black',
                'width': '150px'}
        )

    # Add Tag button
    add_tag_button = dbc.Button(
        "Add Tag", id="add-tag-button", n_clicks=0,
        style={'background-color': '#E9F5FE', 'border': 'none', 'color': 'black', 'width': '150px'}
    )

    # Generate buttons for attributes not in the excluded list
    attribute_buttons = [add_tag_button]  # Start with the Add Tag button
    for attribute, value in song_data.items():
        if attribute not in excluded_attributes:
            attribute_value = song_data.get(attribute, 'None')
            attribute_buttons.append(button_generator(attribute, attribute_value))
    
    # Wrap the buttons in a Div for display
    attributes = html.Div(attribute_buttons, style={
        'display': 'flex',
        'flex-wrap': 'wrap',
        'gap': '10px',
        'justify-content': 'flex-start'})

    return attributes

# Modal resources content (dynamic based on whether the song is in the user's library)


def modal_resources_generator(song_data, track_id):
    lyrics_link = song_data.get('lyrics', '')
    chords_link = song_data.get('chords', '')
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
                        'border': 'none',
                       'color': 'white',
                       'width': '150px'},
                className='info-icon'
            )
        else:
            if link == '': # If no lyrics have been added yet, don't make lyrics clickable
                button = dbc.Button(
                    html.Span(resource_name, style={'fontSize': '16px'}),
                    id={
                        "index": track_id,
                        "type": "edit-resource",
                        "resource": resource_name.lower().replace(" ", "_")
                    },
                    style={'cursor': 'pointer',
                        'background-color': '#f9be82',
                        'color': 'blue',
                        'width': '150px'},
                    className='info-icon'
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
                        'width': '150px'},
                    className='info-icon'
                )
        return button

    lyrics = resource_button_generator(
        "Lyrics", lyrics_link, track_id)
    chords = resource_button_generator(
        "Chords", chords_link, track_id)
    sheet_music = resource_button_generator(
        "Sheet Music", sheet_music_link, track_id)

    resources = dbc.Row(
        html.Div([lyrics, chords, sheet_music], style={
            'display': 'flex',
            'justify-content': 'space-between'}
        ), key=track_id, className='edit-resource')

    return resources

# Row generator


def song_row_generator(track_id, info, page, personal_library=None):
    row_type = f"{page}-row"

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
    ], id={'type': row_type, 'index': track_id}, n_clicks=0, style={'cursor': 'pointer', 'marginLeft': '10px'}), width=4)

    # Accompanying checkmarks per row
    if track_id in personal_library:
        checkbox = dbc.Col(html.Div(
            add_icon_filled,
            id={'type': 'song-check', 'index': track_id},
            n_clicks=0,
            className='resource-icon',
        ), width=2, style={
            'display': 'flex',
            'justify-content': 'center',  # Center horizontally
            'align-items': 'center',  # Center vertically
        })
    else:
        checkbox = dbc.Col(html.Div(
            add_icon_unfilled,
            id={'type': 'song-check', 'index': track_id},
            n_clicks=0,
            className='resource-icon',
        ), width=2, style={
            'display': 'flex',
            'justify-content': 'center',  # Center horizontally
            'align-items': 'center',  # Center vertically
        })

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
    for resource_name in ['lyrics', 'chords', 'sheet_music']:
        if track_id in personal_library and personal_library[track_id][resource_name]!='':
            resource = dbc.Col(html.Button(
                globals()[f"{resource_name}_icon"],
                id={
                    "index": track_id,
                    "type": "edit-resource",
                    "resource": resource_name
                },
                n_clicks=0,
                className='info-icon',
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
            }), className='info-icon',
                style={
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

# Fill in a recommended link
def resource_link_suggestion(resource_type=None, title=None, artist=None):
    if title!=None and artist!=None:
        artist_simple = re.sub(r'[^a-zA-Z0-9 ]', '', artist).lower()
        title_simple = re.sub(r'[^a-zA-Z0-9 ]', '', title).lower()
        if resource_type == 'lyrics':
            artist_simple = artist_simple.replace(' ','')
            title_simple = title_simple.replace(' ','')
            link = f'https://www.azlyrics.com/lyrics/{artist_simple}/{title_simple}.html'
        elif resource_type == 'chords':
            artist_simple = artist_simple.replace(' ','%20')
            title_simple = title_simple.replace(' ','%20')
            link = f'https://www.ultimate-guitar.com/search.php?search_type=title&value={artist_simple}%20{title_simple}'
        elif resource_type == 'sheet_music':
            artist_simple = artist_simple.replace(' ','+')
            title_simple = title_simple.replace(' ','+')
            link = f'https://www.musicnotes.com/search/go?w={artist_simple}+{title_simple}&from=header'
    else:
        link = None

    return link