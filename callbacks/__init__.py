"""
callbacks/__init__.py

Registers all callback functions for the Dash application by importing and calling registration functions from other callback modules.

Functions:
    - register_callbacks(app): Registers all callbacks for the app.
"""

from .input_modal_callbacks import register_input_modal_callbacks
from .info_modal_callbacks import register_info_modal_callbacks
from .library_page import register_library_page_callbacks
from .search_page import register_search_page_callbacks
from .personal_library import register_personal_library_callbacks
from .page_display import register_page_display_callbacks  # Import the combined display_page callback

def register_callbacks(app):
    register_input_modal_callbacks(app)
    register_info_modal_callbacks(app)
    register_library_page_callbacks(app)
    register_search_page_callbacks(app)
    register_personal_library_callbacks(app)
    register_page_display_callbacks(app)  # Register the combined display_page callback
