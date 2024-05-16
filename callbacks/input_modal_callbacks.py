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
        ],
        [
            Input({"type": "edit-resource", "index": ALL,
                  "resource": ALL}, "n_clicks")
        ],
        [
            State("input-modal-status", "is_open"),
            State("user-library-store", "data")
        ],
        prevent_initial_call=True
    )
    def toggle_update_input_modal(resource_clicks, is_open, library_data):
        ctx = callback_context
        if not ctx.triggered:
            return is_open

        trigger_info = ast.literal_eval(
            ctx.triggered[0]["prop_id"].split('.')[0])
        resource_type = trigger_info["resource"]
        track_id = trigger_info["index"]

        existing_link = library_data[track_id]
        input_bar = dbc.Input(
            id=existing_link,
            placeholder="Insert link",
            type="text",
            style={
                'flexGrow': 1,
                'margin-right': '10px'}),
        submit_button = dbc.Button(
            "Submit",
            id={
                'type': 'submit-link',
                'index': track_id,
                'resource': resource_type},
            className="ms-auto",
            n_clicks=0
        )
        input_components = html.Div([input_bar, submit_button], style={
            'display': 'flex',
            'flexWrap': 'nowrap'
        })

        if any(click > 0 for click in resource_clicks):
            return not is_open, input_components
        return is_open, no_update
