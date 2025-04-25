import dash
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from climate.callbacks import *
from climate.frontend import*
import climate.frontend as frontend
import dash_bootstrap_components as dbc
import dash_daq as daq
import climate.frontend as fr




# Dash-App initialisieren
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Für Deployment benötigt


def main():
    app.layout = fr.init_applayout()
    register_callbacks(app)
    app.run(debug=False)

if __name__ == "__main__":
    main()