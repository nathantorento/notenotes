"""
components/info_modal.py

Defines the info modal component used in the Dash application. This modal is imported and used in the layout and callbacks.

Defines:
    - info_modal: The info modal component.
"""

from dash import html
import dash_bootstrap_components as dbc
from utils.icons import edit_icon

info_modal = dbc.Modal(
    [
        dbc.ModalHeader(
            dbc.Row(
                [
                    dbc.Col(dbc.ModalTitle("Metadata"), width=6),
                    dbc.Col(
                        html.Button(
                            edit_icon,
                            id="edit-modal-icon", n_clicks=0, style={
                                'border': 'none',
                                'background': 'none',
                                'cursor': 'pointer'}
                        ),
                        style={'display': 'flex', 'margin-left': '5px'}
                    )
                ],
            ),
            close_button=True
        ),
        dbc.ModalBody([
            html.Div(id="modal-attributes"),
            # Space between attributes and resources
            html.Div(style={"height": "20px"}),
            html.Div(id="modal-resources")
        ]),
    ],
    id="modal-status",
    is_open=False,  # Initially don't show the modal
    centered=True,
    backdrop=True,  # Allow dismissal by clicking outside of modal
    className="base-modal"  # CSS class to determine z-index and display priority
)
