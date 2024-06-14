"""
callbacks/info_modal.py

Defines callback functions related to the info modal in the Dash application.

Functions:
    - register_info_modal_callbacks(app): Registers callbacks related to the info modal.
"""

import dash
from dash.dependencies import Input, Output, State, ALL
from dash import callback_context, no_update
import ast
import pandas as pd
from app import app
from utils.helpers import modal_attributes_generator, modal_resources_generator

# Load the pre-processed data
sample_database = pd.read_csv('data/sample_database.csv')


def register_info_modal_callbacks(app):

    @app.callback(
        [
            Output("modal-status", "is_open"),
            Output('modal-attributes', 'children'),
            Output('modal-resources', 'children')
        ],
        [
            Input({'type': 'search-row', 'index': ALL}, 'n_clicks'),
            Input({'type': 'library-row', 'index': ALL}, 'n_clicks'),
            Input({'type': 'edit-icon', 'index': ALL}, 'n_clicks'),
            Input({'type': 'submit-link', 'index': ALL, 'resource': ALL}, 'n_clicks'),
        ],
        [
            State("modal-status", "is_open"),
            State('user-library-store', 'data')
        ],
        prevent_initial_call=True
    )
    def toggle_update_modal(search_row_clicks, library_row_clicks, edit_icon_clicks, submit_link_clicks, is_open, personal_library):
        ctx = callback_context
        if not ctx.triggered:
            return is_open, no_update, no_update

        triggered_element = ctx.triggered[0]['prop_id']
        index = ast.literal_eval(triggered_element.split('.')[0])['index']

        # Retrieve song data, checking personal library first
        if personal_library.get(index):
            song_data = personal_library.get(index)
        else:
            song_data = sample_database[sample_database['track_id'] == index].drop(
            columns='track_id').iloc[0].to_dict()

        # Refresh info modal if submit-link is clicked
        if any(click > 0 for click in submit_link_clicks):
            modal_attributes = modal_attributes_generator(song_data)
            modal_resources = modal_resources_generator(song_data, index) if index in personal_library else []
            return is_open, modal_attributes, modal_resources
        
        # Modal content generation based on the song data and whether it is in the library
        if any(click > 0 for click in search_row_clicks + library_row_clicks + edit_icon_clicks):
            if song_data:
                modal_attributes = modal_attributes_generator(song_data)
                modal_resources = modal_resources_generator(
                    song_data, index) if index in personal_library else []
                return not is_open, modal_attributes, modal_resources
            else:
                return not is_open, no_update, no_update
        return is_open, no_update, no_update
    
    # @app.callback(
    #     [Output("add-tag-button", "style"),
    #     Output("tag-input", "style")],
    #     [Input("add-tag-button", "n_clicks")],
    #     [State("add-tag-button", "style"), State("tag-input", "style")]
    # )
    # def toggle_tag_input(n_clicks, btn_style, input_style):
    #     if n_clicks > 0:
    #         return {'display': 'none'}, {}  # Hide button, show input
    #     return btn_style, input_style  # No change to styles if not clicked

    # @app.callback(
    #     [Output("tags-container", "children"),
    #     Output("add-tag-button", "n_clicks"),
    #     Output("tag-input", "value"),
    #     Output("tag-input", "style")],
    #     [Input("tag-input", "n_submit"), Input("tag-input", "n_blur")],
    #     [State("tag-input", "value"), State("tags-container", "children")]
    # )
    # def add_tag(submit, blur, tag_value, existing_tags):
    #     triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    #     if triggered_id == "tag-input" and (submit or blur):
    #         if tag_value:  # Only add tag if there's some text entered
    #             new_tag = dbc.Button(tag_value, className="m-1")
    #             existing_tags.append(new_tag)
    #             return existing_tags, 0, '', {'display': 'none'}  # Reset
    #     raise PreventUpdate
