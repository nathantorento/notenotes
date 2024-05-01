import dash
from dash import html, dcc, Dash, Input, Output, State, callback_context, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import os
import base64
from requests import post, get
import json

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Initialize the Dash app with Bootstrap CSS
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("NoteNotes", className="display-4", style={'fontSize': '24px', 'text-align': 'center'}),
                html.Hr(),
                dbc.Nav([
                    dbc.NavLink("Search", href="/", active="exact"),
                    dbc.NavLink("Library", href="#", active="exact"),
                ], vertical=True, pills=True),
                html.Hr(),
                dbc.Nav([
                    dbc.NavLink("User", href="#", active="exact"),
                    html.Div(className="bi bi-person-circle")
                ], vertical=True, pills=True),
            ], width=2, style={'backgroundColor': '#ADD8E6', 'height': '100vh'}),
            dbc.Col([
                dcc.Input(id="artist-input", type="text", placeholder="Enter artist name", debounce=True, style={'marginLeft': '30px'}),
                html.Button("Search", id="search-button"),
                
                html.Div(id="songs-output"),
            ], width=10),
        ], className="g-0"),
    ], fluid=True),
], style={'margin': '10px'})

# Functions to interact with Spotify API
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    return json_result["access_token"]

def get_songs_by_artist(artist_name):
    token = get_token()
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    headers = {"Authorization": "Bearer " + token}
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    artist_id = json_result["artists"]["items"][0]["id"] if json_result["artists"]["items"] else None
    if artist_id:
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        return json_result["tracks"]
    return []

@app.callback(
    Output('songs-output', 'children'),
    Input('search-button', 'n_clicks'),
    State('artist-input', 'value')
)
def update_output(n_clicks, value):
    if n_clicks is None or not value:
        raise PreventUpdate
    songs = get_songs_by_artist(value)
    return html.Ul([html.Li(f"{song['name']} - {song['artists'][0]['name']}", style={'listStyleType': 'none'}) for song in songs])

if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
