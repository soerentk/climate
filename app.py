import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Daten einlesen (vorherigen Code anpassen)
def load_data():
    df = pd.read_csv(
        "data/dataset-average-anomaly.txt",
        comment="%",
        delim_whitespace=True,
        names=["Date Number", "Year", "Month", "Day", "Day of Year", "Anomaly"],
        header=None
    )
    df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])
    return df

df = load_data()

# Dash-App initialisieren
app = dash.Dash(__name__)
server = app.server  # Für Deployment benötigt

# Layout der App
app.layout = html.Div([
    html.H1("Klimawandel-Analyse", style={"textAlign": "center", "color": "#2c3e50"}),
    
    html.Div([
        dcc.Dropdown(
            id="chart-selector",
            options=[
                {"label": "Tägliche Anomalien", "value": "daily"},
                {"label": "Monatliche Durchschnitte", "value": "monthly"},
                {"label": "Jährlicher Trend", "value": "yearly"}
            ],
            value="daily",
            style={"width": "300px"}
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
])

# Callbacks für Interaktivität
@app.callback(
    [Output("main-chart", "figure"),
     Output("heatmap", "figure")],
    [Input("chart-selector", "value"),
     Input("year-slider", "value")]
)
def update_charts(selected_chart, years):
    filtered_df = df[(df["Year"] >= years[0]) & (df["Year"] <= years[1])]
    
    # Hauptchart
    if selected_chart == "daily":
        fig_main = px.line(
            filtered_df,
            x="Date",
            y="Anomaly",
            title="Tägliche Temperaturanomalien",
            labels={"Anomaly": "Abweichung (°C)"}
        )
    elif selected_chart == "monthly":
        monthly = filtered_df.groupby(["Year", "Month"])["Anomaly"].mean().reset_index()
        fig_main = px.bar(
            monthly,
            x="Year",
            y="Anomaly",
            color="Month",
            title="Monatliche Durchschnittsabweichungen",
            color_continuous_scale="Portland"
        )
    else:
        yearly = filtered_df.groupby("Year")["Anomaly"].mean().reset_index()
        fig_main = px.scatter(
            yearly,
            x="Year",
            y="Anomaly",
            trendline="lowess",
            title="Jährlicher Trend mit Glättung"
        )
    
    # Heatmap
    heatmap_df = filtered_df.groupby(["Year", "Month"])["Anomaly"].mean().reset_index()
    heatmap_fig = px.density_heatmap(
        heatmap_df,
        x="Year",
        y="Month",
        z="Anomaly",
        nbinsx=30,
        nbinsy=12,
        color_continuous_scale="RdBu_r",
        title="Monatliche Anomalien Heatmap"
    )
    
    return fig_main, heatmap_fig

# App starten
if __name__ == "__main__":
    app.run_server(debug=True)