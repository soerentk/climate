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
# Annahme: df_temp enthält Temperaturdaten, df_co2 enthält CO₂-Daten
# Beispiel-Datenstruktur:

def load_data():
    # CO₂-Data
    df_co2 = pd.read_csv(
        "data/dataset-co2.txt",
        comment='#',
        sep='\s+',
        header=None,
        names=['year', 'co2_ppm', 'unc']
    )
    
    # Anomaly-Data
    df_temp = pd.read_csv(
        "data/dataset-average-anomaly.txt",
        comment='%',
        sep='\s+',
        header=None,
        names=['date_num', 'year', 'month', 'day', 'doy', 'anomaly']
    )
    
    # Annual mean
    annual_temp = df_temp.groupby('year')['anomaly'].mean().reset_index()
    
    # combinating at 1959
    return pd.merge(
        annual_temp[annual_temp['year'] >= 1959],
        df_co2,
        on='year',
        how='inner'
    )

df = load_data()

boolean_switch = daq.BooleanSwitch(id='my-boolean-switch', on=True, color="#99c000", className="switch")


def init_applayout():
    app_layout = html.Div([
       html.H1("Climate Analysis", style={'textAlign': 'center', 'padding': '20px', "color": "#99c000"}),
       dcc.Store(id="theme", data=1),
       html.Div(className="switch", style={
                    "margin-right": "20px",
                    "display": "right",
                    "alignItems": "right",
                    "gap": "5px"

                }, children=[
                    boolean_switch,

                ]),
    dcc.Dropdown(
        id='data-selector',
        options=[
            {'label': 'Both Data', 'value': 'both'},
            {'label': 'Anomaly of temperature', 'value': 'temp'},
            {'label': 'CO₂-Concentration', 'value': 'co2'}
        ],
        value='both',
        style={'width': '50%', 'margin': '20px auto'}
    ),
    
    dcc.Graph(id='climate-graph'),
    
    dcc.RangeSlider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=[df['year'].min(), df['year'].max()],
        marks={str(year): str(year) for year in range(1959, 2025, 10)},
        step=1
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
        ]
        ,
        id="wholepage"
    )
    return app_layout