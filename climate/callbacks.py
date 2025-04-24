from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import app

@app.callback(
    Output("graph", "figure"),
    Input("selection", "value"))
def display_animated_graph(selection):
    df = px.data.gapminder() # replace with your own data source
    animations = {
        'GDP - Scatter': px.scatter(
            df, x="gdpPercap", y="lifeExp", animation_frame="year",
            animation_group="country", size="pop", color="continent",
            hover_name="country", log_x=True, size_max=55,
            range_x=[100,100000], range_y=[25,90]),
        'Population - Bar': px.bar(
            df, x="continent", y="pop", color="continent",
            animation_frame="year", animation_group="country",
            range_y=[0,4000000000]),
    }
    return animations[selection]
