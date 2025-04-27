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
    Output('climate-graph', 'figure'),
    [Input('data-selector', 'value'),
     Input('year-slider', 'value'),
     Input("theme", "data"),]
    )
    def update_graph(selected_data, years, theme_value):

        if theme_value == 1:
            template = "plotly"
        if theme_value == 2:
            template = "plotly_dark"
        if theme_value == 3:
            template = "plotly_dark"

        filtered = df[(df['year'] >= years[0]) & (df['year'] <= years[1])]
        
        fig = go.Figure()
        
        # Temperaturanomalie
        fig.add_trace(go.Scatter(
            x=filtered['year'],
            y=filtered['anomaly'],
            name='Temperaturanomalie (°C)',
            line=dict(color='#e74c3c'),
            visible=selected_data in ['both', 'temp'],
            yaxis='y1'
        ))
        
        # CO₂-Hauptlinie
        fig.add_trace(go.Scatter(
            x=filtered['year'],
            y=filtered['co2_ppm'],
            name='CO₂ (ppm)',
            line=dict(color='#3498db'),
            visible=selected_data in ['both', 'co2'],
            yaxis='y2'
        ))
        
        # CO₂-Unsicherheitsbereich
        fig.add_trace(go.Scatter(
            x=filtered['year'].tolist() + filtered['year'].tolist()[::-1],
            y=(filtered['co2_ppm'] + filtered['unc']).tolist() + 
            (filtered['co2_ppm'] - filtered['unc']).tolist()[::-1],
            fill='toself',
            fillcolor='rgba(52, 152, 219, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='CO₂-unc',
            showlegend=False,
            visible=selected_data in ['both', 'co2'],
            yaxis='y2'
        ))
        
        fig.update_layout(
            title=f'Climate-Data {years[0]}-{years[1]}',
            xaxis_title='Year',
            yaxis=dict(
                title='anomalie of temperatur (°C)',
                # titlefont=dict(color='#e74c3c'),
                # tickfont=dict(color='#e74c3c'),
                range=[df['anomaly'].min()-0.1, df['anomaly'].max()+0.1]
            ),
            yaxis2=dict(
                title='CO₂-Conzentration (ppm)',
                # titlefont=dict(color='#3498db'),
                # tickfont=dict(color='#3498db'),
                overlaying='y',
                side='right',
                range=[df['co2_ppm'].min()-10, df['co2_ppm'].max()+10]
            ),
            hovermode='x unified',
            legend=dict(x=0.05, y=0.95),
            template=template,
            margin=dict(l=70, r=70, t=70, b=70)
        )
        
        return fig
    
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
    [Output('data-selector', 'style'),
    Output('data-selector', 'className'),],
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
        
    

 

