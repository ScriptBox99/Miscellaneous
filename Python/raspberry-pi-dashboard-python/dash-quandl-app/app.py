import dash
import dash_core_components as dcc
import dash_html_components as html

import colorlover as cl
import datetime as dt
import flask
import os
import pandas as pd
from pandas_datareader.data import DataReader
import time

app = dash.Dash('stock-tickers')
server = app.server

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-latest.min.js' 

colorscale = cl.scales['9']['qual']['Paired']

df_symbol = pd.read_csv('tickers.csv')

app.layout = html.Div([
    html.Div([
        html.H2('Finance Dashboard', # Header title
                style={'display': 'inline',
                       'float': 'left',
                       'font-size': '2.65em',
                       'margin-left': '7px',
                       'font-weight': 'bolder',
                       'font-family': 'Product Sans',
                       'color': "rgba(117, 117, 117, 0.95)",
                       'margin-top': '20px',
                       'margin-bottom': '0'
                       })
    ]),
    dcc.Dropdown(
        id='stock-ticker-input',
        options=[{'label': s[0], 'value': str(s[1])}
                 for s in zip(df_symbol.Company, df_symbol.Symbol)],
        value=[], # replace with desired default tickets e.g. - value=['AAPL','GOOG'],
        multi=True
    ),
    html.Div(id='graphs')
], className="container")

def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std  = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band
    
@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value')])
def update_graph(tickers):
    graphs = []
    try:
        for i, ticker in enumerate(tickers):
            try:
                df = DataReader(str(ticker), 'quandl',
                                dt.datetime(2017, 1, 1),
                                dt.datetime.now(),
                                retry_count=0).reset_index()
            except Exception as e:
                graphs.append(html.H3(
                    'Data is not available for {}, please retry later.'.format(ticker),
                    style={'marginTop': 20, 'marginBottom': 20}
                ))
                graphs.append(html.H3(
                    'Exception {}'.format(e),
                    style={'marginTop': 20, 'marginBottom': 20}
                ))
                continue

            candlestick = {
                'x': df['Date'],
                'open': df['Open'],
                'high': df['High'],
                'low': df['Low'],
                'close': df['Close'],
                'type': 'candlestick',
                'name': ticker,
                'legendgroup': ticker,
                'increasing': {'line': {'color': colorscale[0]}},
                'decreasing': {'line': {'color': colorscale[1]}}
            }
            bb_bands = bbands(df.Close)
            bollinger_traces = [{
                'x': df['Date'], 'y': y,
                'type': 'scatter', 'mode': 'lines',
                'line': {'width': 1, 'color': colorscale[(i*2) % len(colorscale)]},
                'hoverinfo': 'none',
                'legendgroup': ticker,
                'showlegend': True if i == 0 else False,
                'name': '{} - bollinger bands'.format(ticker)
            } for i, y in enumerate(bb_bands)]
            try:
                graphOutput = dcc.Graph(
                    id=ticker,
                    figure={
                        'data': [candlestick] + bollinger_traces,
                        'layout': {
                            'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                            'legend': {'x': 0}
                        }
                    }
                )
				
				# WARNING: If the plotly dash code is acting up this line will typically cause all enumeration to stop. 
                graphs.append(html.Div(graphOutput))
            except Exception as e:
                graphs.append(html.H3(
                        'Graph Exception {}'.format(e),
                        style={'marginTop': 20, 'marginBottom': 20}
                    ))
    except Exception as e:
        graphs.append(html.H3(
                    'Overall Exception {}'.format(e),
                    style={'marginTop': 20, 'marginBottom': 20}
                ))
    return graphs


external_css = ["https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2cc54b8c03f4126569a3440aae611bbef1d7a5dd/stylesheet.css"]

for css in external_css:
    app.css.append_css({"external_url": css})


if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })


if __name__ == '__main__':
    app.run_server(debug=True)
    
