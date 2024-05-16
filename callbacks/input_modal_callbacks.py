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


def register_input_modal_callbacks(app):

    @app.callback(
        [
            Output("input-modal-status", "is_open"), # output with existing link filled in (or not)
            Output("input-modal-components", "children"),
            Output("editing-resource-type", "children"),
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
            return is_open

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

        resource_name = resource_type.replace('_',' ').title()
        input_heading = html.Div(html.A(resource_name, href=existing_link))

        if any(click > 0 for click in resource_clicks):
            return (not is_open, input_components, input_heading) # Open the modal if a resource button was clicked
        
        elif any(click > 0 for click in submit_clicks):
            return (False, no_update, input_heading)  # Close the modal if submit was clicked

        return (is_open, no_update, no_update) # Don't change anything if nothing is triggered
