"""
components/input_modal.py

Defines the input modal component used in the Dash application. This modal is imported and used in the layout and callbacks.

Defines:
    - input_modal: The input modal component.
"""

from dash import html
import dash_bootstrap_components as dbc
from utils.styles import modal_display_style

input_modal = dbc.Modal(
    [
        dbc.ModalHeader(
            [
                html.Div([
                    dbc.Row([
                        dbc.Col(
                            dbc.ModalTitle(id="editing-resource-type"),
                            width=10
                        ),
                        dbc.Col(
                            dbc.Button(
                                "[Add Suggested Link?]", 
                                id="suggested-link-button", 
                                n_clicks=0,
                                style={
                                    'margin-left': '10px',
                                    'background': '#E3EBF1',
                                    'fontSize': '14px',
                                    'border': 'none',
                                    # 'textDecoration': 'underline',
                                    'color': '#0052B5',
                                    'cursor': 'pointer'
                                } 
                            ), 
                            width=10
                        )
                    ], style={'display': 'flex', 'flexWrap': 'nowrap'}),
                    dbc.Tooltip(
                        "Click to add the suggested link", 
                        id="suggested-link-tooltip", 
                        target="suggested-link-button", 
                        placement="bottom",
                    ),
                    html.P("(Consider opening the link in a new tab)", style={'fontSize': '12px', 'margin': '0', 'color':'#95CDF6'})
                ], style={'display': 'flex', 'flexDirection': 'column'}),
            ], close_button=True
        ),
        dbc.ModalBody([
            html.Div(id="input-modal-components")
        ], style = modal_display_style),
    ],
    id="input-modal-status",
    is_open=False,
    centered=True,
    backdrop=True,
    className="input-modal"  # CSS class to determine z-index and display priority
)
