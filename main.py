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
app.layout = html.Div(children=[html.H1('Crypto predicting challange',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.P("timerange"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='time-range',
                                                min=1567296000,max=1570665600,step=50000,
                                                marks={
                                                    1567296000:"0D",
                                                    1568073600:"10D",
                                                    1568937600:"20D",
                                                    1569801600:"30D",
                                                    1570665600:"40D"},
                                                value=[1567296000, 1568073600]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='time-range', component_property='value'))
def get_scatter_chart(rang):
    data = coin.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='usd', from_timestamp=rang[0], to_timestamp=rang[1])
    prices = data['prices']
    x=[]
    for i in prices:
        x.append(i[1])
        prices = x
    print(prices)
    fig = px.line(y=prices)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

