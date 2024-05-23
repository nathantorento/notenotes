"""
callbacks/input_modal.py

Defines callback functions related to the input modal in the Dash application.

Functions:
    - register_input_modal_callbacks(app): Registers callbacks related to the input modal.
"""

from dash.dependencies import Input, Output, State, ALL
from dash import callback_context, no_update, html
import dash_bootstrap_components as dbc
import ast
from app import app
from utils.helpers import resource_link_suggestion


def register_input_modal_callbacks(app):

    @app.callback(
        [
            Output("input-modal-status", "is_open"), # output with existing link filled in (or not)
            Output("input-modal-components", "children"),
            Output("editing-resource-type", "children"),
            Output("suggested-link-tooltip", "children"),  # Tooltip content
        ],
        [
            Input({"type": "edit-resource", "index": ALL, "resource": ALL}, "n_clicks"),
            Input({'type': 'submit-link', 'index': ALL, 'resource': ALL}, "n_clicks"),
        ],
        [
            State("input-modal-status", "is_open"),
            State("user-library-store", "data")
        ],
        prevent_initial_call=True
    )
    def toggle_update_input_modal(resource_clicks, submit_clicks, is_open, library_data):
        ctx = callback_context
        if not ctx.triggered:
            return (is_open, no_update, no_update, no_update)

        trigger_info = ast.literal_eval(
            ctx.triggered[0]["prop_id"].split('.')[0])
        resource_type = trigger_info["resource"]
        track_id = trigger_info["index"]

        existing_link = library_data[track_id][resource_type]

        input_bar = dbc.Col(
            dbc.Input(
                id='input-link',
                value=existing_link,
                placeholder="Insert link",
                type="text",
                style={
                    'flexGrow': 1,
                    'margin-right': '10px'}
            ), width=9, style={'margin-right': '10px'}
        )
        submit_button = dbc.Col(
            dbc.Button(
                "Submit",
                id={
                    'type': 'submit-link',
                    'index': track_id,
                    'resource': resource_type,
                },
                # className="submit-link",
                n_clicks=0
            ), width=2
        )

        input_components = dbc.Row(
            html.Div([input_bar, submit_button], style={
            'display': 'flex',
            'justify-content': 'space-between'
            }
        ), key=track_id)
        
        track_title = library_data[track_id]['title']
        track_artist = library_data[track_id]['artist']
        suggested_link = resource_link_suggestion(resource_type, track_title, track_artist)
        if suggested_link:
            tooltip_content = suggested_link
        else:
            tooltip_content = "No automated link generated for this song."
        
        resource_name = resource_type.replace('_',' ').title()

        if existing_link == '': # Don't make input heading clickable if existing link is empty
            input_heading = html.Div(html.A(resource_name))
        else:
            input_heading = html.Div([
                html.A(resource_name, href=existing_link),
            ])

        if any(click > 0 for click in resource_clicks):
            return (not is_open, input_components, input_heading, tooltip_content) # Open the modal if a resource button was clicked
        
        elif any(click > 0 for click in submit_clicks):
            return (False, no_update, no_update, no_update)  # Close the modal if submit was clicked

        return (is_open, no_update, no_update, no_update) # Don't change anything if nothing is triggered

    @app.callback(
        Output('input-link', 'value'),
        [
            Input('suggested-link-button', 'n_clicks'),
            Input("suggested-link-tooltip", "children"),  # Tooltip content
        ],
        prevent_initial_call=True
    )
    def fill_suggested_link(n_clicks, suggested_link):
        if n_clicks:
            if suggested_link != "No automated link generated for this song.":
                return suggested_link
        return no_update
