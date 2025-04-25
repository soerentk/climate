import dash
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import climate.frontend as frontend
import dash_bootstrap_components as dbc
import dash_daq as daq

# TODO Durschnitsanomalien des Jahres als graph darstellen
# TODO CO2 Belastung dataset finden
# TODO CO2 Set über anomalie set legen und korrelationen zu verdeutlichen


def load_data():
    df = pd.read_csv(
        "data/dataset-average-anomaly.txt",
        comment="%",
        sep='\s+',
        names=["Date Number", "Year", "Month", "Day", "Day of Year", "Anomaly"],
        header=None
    )
    df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])
    return df

df = load_data()

def average_anomalia_per_year():
    df2 = pd.read_csv(
        "data/dataset-average-anomaly.txt",
        comment="%",
        sep='\s+',
        names=["Date Number", "Year", "Month", "Day", "Day of Year", "Anomaly"],
        header=None
    )
    df2["Anomaly"] = 
    df2["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])
    return df2


boolean_switch = daq.BooleanSwitch(id='my-boolean-switch', on=False, color="#99c000", className="switch")

def init_applayout():

    app_layout = html.Div(
    [
    html.H1("Climate Change Analysis", style={"textAlign": "center", "color": "#99c000"}),
    dcc.Store(id="theme", data=0),
    html.Div([
        html.Div(className="switch", style={
                    "margin-right": "20px",
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "5px"

                }, children=[
                    boolean_switch,

                ]),
        dcc.Dropdown(
            id="chart-selector",
            options=[
                {"label": "Tägliche Anomalien", "value": "daily"},
                {"label": "Monatliche Durchschnitte", "value": "monthly"},
                {"label": "Jährlicher Trend", "value": "yearly"}
            ],
            value="daily",
            style={"width": "300px"},
            className="light_mode",
        ),
        
        dcc.RangeSlider(
            id="year-slider",
            min=df["Year"].min(),
            max=df["Year"].max(),
            step=10,
            value=[1950, 2020],
            marks={year: str(year) for year in range(1880, 2030, 20)}
        )
        ], style={"padding": "20px"}),

        dcc.Graph(id="main-chart"),

        dcc.Graph(id="heatmap")
        ]
        ,
        id="wholepage"
    )
    return app_layout