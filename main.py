"""
main.py

This is the entry point of the Dash application. It sets the app layout,
registers all callbacks, and runs the server.

Imports:
    - app from app: The Dash application instance.
    - layout from layout: The layout of the app.
    - register_callbacks from callbacks: Function to register all callbacks.

Usage:
    Run this script to start the Dash application.
"""
from app import app
from layout import layout
from callbacks import register_callbacks

app.layout = layout
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
