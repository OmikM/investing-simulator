from optparse import Values
from tkinter import Y
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
from pycoingecko import CoinGeckoAPI


coin = CoinGeckoAPI()

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,max=10000,step=2500,
                                                marks={
                                                    0:"0",
                                                    2500:"2500",
                                                    5000:"5000",
                                                    7500:"7500",
                                                    10000:"10000"},
                                                value=[0, 10000]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(data):
    data = coin.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='usd', from_timestamp=1199138400, to_timestamp=1500000000)
    print(data[0])
    fig = px.line(Y=data)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
