import dash
from dash import dcc, html, Input, Output
import plotly.express as px  # Korrekter Import-Name
import pandas as pd
import math

# Dash-App initialisieren
app = dash.Dash(__name__)

# Layout der Anwendung
app.layout = html.Div([
    html.H1("Dash mit Plotly Express", style={'textAlign': 'center'}),  # H1 statt int
    
    dcc.Slider(
        id='freq-slider',  # Einfache Anführungszeichen
        min=1,
        max=10,  # Korrekte Maximalwert
        step=1,
        value=1,
        marks={i: str(i) for i in range(1, 11)},
        tooltip={"placement": "bottom"}  # Korrekte Anführungszeichen
    ),
    
    dcc.Graph(id='example-graph')
])

# Callback für Interaktivität
@app.callback(
    Output('example-graph', 'figure'),
    Input('freq-slider', 'value')
)
def update_graph(freq):
    # Daten mit pandas DataFrame erstellen
    df = pd.DataFrame({
        'x': [i * 0.1 for i in range(100)],  # Korrekte Listengenerierung
        'y': [math.sin(xi * freq) for xi in [i * 0.1 for i in range(100)]]
    })
    
    # Plot mit Plotly Express
    fig = px.line(
        df,
        x='x',  # Korrekte Spaltennamen als Strings
        y='y',
        title=f'Sinuswelle mit Frequenz {freq}',
        labels={'x': 'Zeit', 'y': 'Amplitude'},  # Korrekte Syntax
        template='plotly_white'
    )
    return fig

# Server starten
if __name__ == '__main__':
    app.run_server(debug=True)