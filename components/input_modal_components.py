"""
components/input_modal.py

Defines the input modal component used in the Dash application. This modal is imported and used in the layout and callbacks.

Defines:
    - input_modal: The input modal component.
"""

from dash import html
import dash_bootstrap_components as dbc

input_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle(id="editing-resource-type"), close_button=True),
        dbc.ModalBody([
            html.Div(id="input-modal-components")
        ]),
    ],
    id="input-modal-status",
    is_open=False,
    centered=True,
    backdrop=True,
    className="input-modal"  # CSS class to determine z-index and display priority
)
