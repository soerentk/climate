import dash
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app import app
from climate.frontend import*
import climate.frontend as fr


dark_mode_basic_color = "#000"  # black
dark_mode_basic_blue = "#292544"  # dark blue/purple 
light_mode = "#fff"  # white

light_mode_style = {
    "backgroundColor": light_mode,
    # "color": "#000",
    "border": "1px solid #61830d",  # dark green
    "width": "300px"
}


dark_mode_style_blue = {
    "backgroundColor": dark_mode_basic_blue,
    # "color": "#FFF",
    "border": "1px solid #61830d"  # dark green
}
dark_mode_style_black = {
    "backgroundColor": dark_mode_basic_color,
    # "color": "#FFF",
    "border": "1px solid #61830d",  # dark green
    "width": "300px"

}

def register_callbacks(app):



    @app.callback(
        [Output("main-chart", "figure"),
        Output("heatmap", "figure")],
        [Input("chart-selector", "value"),
        Input("year-slider", "value"),
        Input("theme", "data"),
]
    )
    def update_charts(selected_chart, years, theme_value):
        filtered_df = fr.df[(fr.df["Year"] >= years[0]) & (fr.df["Year"] <= years[1])]
        

        if theme_value == 1:
            template = "plotly"
        if theme_value == 2:
            template = "plotly_dark"
        if theme_value == 3:
            template = "plotly_dark"

        # Hauptchart
        if selected_chart == "daily":
            fig_main = px.line(
                filtered_df,
                x="Date",
                y="Anomaly",
                title="Tägliche Temperaturanomalien",
                labels={"Anomaly": "Abweichung (°C)"},
                template= template
            )
        elif selected_chart == "monthly":
            monthly = filtered_df.groupby(["Year", "Month"])["Anomaly"].mean().reset_index()
            fig_main = px.bar(
                monthly,
                x="Year",
                y="Anomaly",
                color="Month",
                title="Monatliche Durchschnittsabweichungen",
                color_continuous_scale="Portland",
                template=template
            )
        else:
            yearly = filtered_df.groupby("Year")["Anomaly"].mean().reset_index()
            fig_main = px.scatter(
                yearly,
                x="Year",
                y="Anomaly",
                trendline="lowess",
                title="Jährlicher Trend mit Glättung",
                template=template
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
            title="Monatliche Anomalien Heatmap",
            template=template
        )
        
        return fig_main, heatmap_fig



    @app.callback(
        Output('theme', 'data'),
        Input('my-boolean-switch', 'on')
    )
    def update_output(on):
        """
        Updates the theme data based on the state of the boolean switch.

        Parameters:
        -----------
        on : bool
            The state of the boolean switch. If True, dark mode is enabled. If False, light mode is enabled.

        Returns:
        --------
        int
            The theme data. 1 for light mode, 3 for dark mode.
        """

        if on:
            return 3
        elif not on:
            return 1
        

    @app.callback(
        Output('wholepage', 'className'),
        Input('theme', 'data')
    )
    def update_all_style(is_dark_mode):
        """
        Updates the style of the whole page based on the theme data.

        Parameters:
        -----------
        is_dark_mode : int
            The theme data. 1 for light mode, 2 for dark blue mode, 3 for dark mode.

        Returns:
        --------
        str
            The class name corresponding to the selected theme.
        """
        
        if is_dark_mode == 1:
            style = "light_mode"
        if is_dark_mode == 2:
            style = "dark_mode_blue"
        if is_dark_mode == 3:
            style = "dark_mode_basic"

        return style
    
    @app.callback(
        [Output('chart-selector', 'style'),
        Output('chart-selector', 'className'),],
        Input('theme', 'data')
    )
    def dropdown_darkmode(is_dark_mode):
          #style dropdown: for style changes
        if is_dark_mode == 1:
            style_dropdown = light_mode_style
        if is_dark_mode == 2:
            style_dropdown = dark_mode_style_blue
        if is_dark_mode == 3:
            style_dropdown = dark_mode_style_black
        
            # style_dropdown2: for className changes
        if is_dark_mode == 1:
            style_dropdown2 = "light_mode"
        if is_dark_mode == 2:
            style_dropdown2 = "blue_mode"
        if is_dark_mode == 3:
            style_dropdown2 = "dark_mode"

        return [style_dropdown]*1 + [style_dropdown2]*1
        
    

 

