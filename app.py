import plotly
import dash
from dash.dependencies import Input, Output, State, Event
import plotly.plotly as py
from flask import Flask
import plotly.figure_factory as ff
import dash_core_components as dcc
import dash_html_components as html
from sklearn.utils import shuffle
from plotly.graph_objs import *

import pandas as pd
import numpy as np
from copy import deepcopy

diamonds = pd.read_csv("diamonds.csv")
diamonds = shuffle(diamonds)
diamonds = diamonds.reset_index(drop=True)
server = Flask('my app')
server.secret_key = 'secret'

app = dash.Dash('UberApp', server=server)

slider_value = [1, 15000, 35000, 53940]

mappingCut = {
    "Ideal": 5,
    "Premium": 4,
    'Very Good': 3,
    'Good': 2,
    'Fair': 1
}

mappingClarity = {
    "IF": 8,
    "VVS1": 7,
    'VVS2': 6,
    'VS1': 5,
    'VS2': 4,
    'SI1': 3,
    'SI2': 2,
    'I1': 1
}

mappingColor = {
    "J": 7,
    "I": 6,
    'H': 5,
    'G': 4,
    'F': 3,
    'E': 2,
    'D': 1
}

diamonds['cut-labels'] = diamonds['cut']
diamonds['color-labels'] = diamonds['color']
diamonds['clarity-labels'] = diamonds['clarity']
diamonds = diamonds.replace({'cut': mappingCut, 'clarity': mappingClarity, 'color': mappingColor})
print(diamonds)
app.layout = html.Div([
    html.Div([
        html.P("Sample Size"),
        html.P("", id='slider-sample-text'),
        html.Div([
            dcc.Slider(
                id='sameple-slider',
                min=1,
                max=53940,
                marks={1: "1", 10000: "10K", 25000: "20K", 40000: "40K", 53940: "53940"},
                value=1000,
                step=1000
            ),
        ], className = "ten columns"),
        html.Br(),
        html.Br(),
        html.Br(),
        dcc.Checklist(
            id='checklist',
            options=[
                {'label': 'Jitter', 'value': 'jitter'}
            ],
            values=['jitter', 'smooth']
        ),
        html.P("X"),
        dcc.Dropdown(
            id='x-dropdown',
            options=[
                {'label': 'carat', 'value': 'carat'},
                {'label': 'cut', 'value': 'cut'},
                {'label': 'color', 'value': 'color'},
                {'label': 'clarity', 'value': 'clarity'},
                {'label': 'depth', 'value': 'depth'},
                {'label': 'table', 'value': 'table'},
                {'label': 'price', 'value': 'price'},
                {'label': 'x', 'value': 'x'},
                {'label': 'y', 'value': 'y'},
                {'label': 'z', 'value': 'z'}
            ],
            value='carat'
        ),
        html.P("Y"),
        dcc.Dropdown(
            id='y-dropdown',
            options=[
                {'label': 'carat', 'value': 'carat'},
                {'label': 'cut', 'value': 'cut'},
                {'label': 'color', 'value': 'color'},
                {'label': 'clarity', 'value': 'clarity'},
                {'label': 'depth', 'value': 'depth'},
                {'label': 'table', 'value': 'table'},
                {'label': 'price', 'value': 'price'},
                {'label': 'x', 'value': 'x'},
                {'label': 'y', 'value': 'y'},
                {'label': 'z', 'value': 'z'}
            ],
            value='depth'
        ),
        html.P("Color"),
        dcc.Dropdown(
            id='color-dropdown',
            options=[
                {'label': 'None', 'value': 'None'},
                {'label': 'carat', 'value': 'carat'},
                {'label': 'cut', 'value': 'cut'},
                {'label': 'color', 'value': 'color'},
                {'label': 'clarity', 'value': 'clarity'},
                {'label': 'depth', 'value': 'depth'},
                {'label': 'table', 'value': 'table'},
                {'label': 'price', 'value': 'price'},
                {'label': 'x', 'value': 'x'},
                {'label': 'y', 'value': 'y'},
                {'label': 'z', 'value': 'z'}
            ],
        ),
        html.P("Facet Row"),
        dcc.Dropdown(
            id='facet-row-dropdown',
            options=[
                {'label': 'None', 'value': 'None'},
                {'label': 'cut', 'value': 'cut-labels'},
                {'label': 'color', 'value': 'color-labels'},
                {'label': 'clarity', 'value': 'clarity-labels'}
            ],
            value="None"
        ),
        html.P("Facet Column"),
        dcc.Dropdown(
            id='facet-col-dropdown',
            options=[
                {'label': 'None', 'value': 'None'},
                {'label': 'cut', 'value': 'cut-labels'},
                {'label': 'color', 'value': 'color-labels'},
                {'label': 'clarity', 'value': 'clarity-labels'}
            ],
            value="None"
        ),
    ], className="two columns",
        style={
                'padding': '20px 20px',
                'background': '#DDE6F0',
                'min-height': '1400px'
        }),
    html.Div([
            dcc.Graph(id='facet-grid'),
            dcc.Graph(id='volume-graph')
    ], className="ten columns")
], className="twelve columns app", style={'margin-left': '-10px', 'background': '#FBFBFB'})


def jitter(dataFrame, x, y):
    dfCopy = deepcopy(dataFrame)
    if (discrete(x) and not discrete(y)) or (not discrete(x) and discrete(y)):
        if(discrete(x)):
            dfCopy[x] = dfCopy[x] + np.random.uniform(-0.4, 0.4, len(dfCopy[x]))
        else:
            dfCopy[y] = dfCopy[y] + np.random.uniform(-0.4, 0.4, len(dfCopy[y]))
    elif(discrete(x) and discrete(y)):
        dfCopy[y] = dfCopy[y] + np.random.uniform(-0.4, 0.4, len(dfCopy[y]))
        dfCopy[x] = dfCopy[x] + np.random.uniform(-0.4, 0.4, len(dfCopy[y]))
    else:
        dfCopy[y] = dfCopy[y] * np.random.uniform(.998, 1.002, len(dfCopy[y]))
        dfCopy[x] = dfCopy[x] * np.random.uniform(.998, 1.002, len(dfCopy[y]))
    return dfCopy

def discrete(name):
    if name == 'cut' or name == 'clarity' or name == 'color':
        return True
    else:
        return False


@app.callback(Output("slider-sample-text", "children"),
              [Input("sameple-slider", "value")])
def drawVolumeGraph(value):
    return str(value)

@app.callback(Output("volume-graph", "figure"),
              [Input("facet-grid", "hoverData")], [State('sameple-slider', 'value')])
def drawVolumeGraph(hoverData, slider_value):
    index = hoverData['points'][0]['pointNumber']
    indexOffset = index
    if index > slider_value:
        index = index - slider_value
        indexOffset = index
    if index+20 > slider_value:
        indexOffset = slider_value-20
    elif index-20 < 0:
        indexOffset = 20
    zVal = []
    for i in range(indexOffset-20, indexOffset+20, 1):
        zVal.append(i)
    xVal = diamonds.iloc[indexOffset-20:indexOffset+20]['x']
    yVal = diamonds.iloc[indexOffset-20:indexOffset+20]['y']
    priceVal = diamonds.iloc[indexOffset-20:indexOffset+20]['price']
    caratVal = diamonds.iloc[indexOffset-20:indexOffset+20]['carat']
    lengthWidthRatio = (xVal/yVal)
    colorVal = []
    for i in zVal:
        if(i == index):
            colorVal.append("rgb(119, 150, 203, 0.5)")
        else:
            colorVal.append("rgb(163, 188, 249, 0.5)")
    trace1 = Bar(
            x=zVal,
            y=lengthWidthRatio,
            marker=dict(
                color=colorVal
            ),
            name='Len/Width'
        )
    trace2 = Scatter(
            x=zVal,
            y=priceVal/caratVal,
            mode='lines+markers',
            marker=dict(
                color='#F9B9F2'
            ),
            yaxis='y2',
            name='Price/Carat'
        )

    fig = Figure(
        data=[trace1, trace2],
        layout=dict(
            title="Metrics vs Forty Closely Sampled Diamonds",
            paper_bgcolor="#FBFBFB",
            bargap=0.01,
            bargroupgap=0,
            showlegend=False,
            yaxis=dict(
                title='Length to Width Ratio',
                range=[0, 3],
                showgrid=False
            ),
            yaxis2=dict(
                title = 'Price per Carat',
                side='right',
                zeroline=False,
                gridcolor="#FBFBFB",
                overlaying='y'
            ),
            xaxis=dict(
                range=[zVal[0]-0.5, zVal[len(zVal)-1]+0.5],
                gridcolor="#FBFBFB",
                title="Diamond Index",
                nticks=41
            )
        )
    )

    return fig


def relabel(x, fig, i):
    if i is 0:
        val = 'xaxis'
    else:
        val = 'yaxis'

    if x == 'color':
        for x in fig['layout']:
            if val in x:
                fig['layout'][x]['range'] = [0.5, 7.5]
                fig['layout'][x]['tickvals'] = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7]
                fig['layout'][x]['ticktext'] = ["J", "", "I", "", "H", "", "G", "", "F", "", "E", "", "D"]
    if x == 'cut':
        for x in fig['layout']:
            if val in x:
                fig['layout'][x]['range'] = [0.5, 5.5]
                fig['layout'][x]['tickvals'] = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
                fig['layout'][x]['ticktext'] = ["Fair", "", "Good", "", "Very Good", "", "Premium", "", "Ideal"]
    if x == 'clarity':
        for x in fig['layout']:
            if val in x:
                fig['layout'][x]['range'] = [0.5, 8.5]
                fig['layout'][x]['tickvals'] = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]
                fig['layout'][x]['ticktext'] = ["I1", "", "SI2", "", "SI1", "", "VS2", "", "VS1", "", "VVS2", "", "VVS1", "", "IF"]



@app.callback(Output("facet-grid", "figure"),
              [Input("x-dropdown", "value"), Input("y-dropdown", "value"),
               Input("color-dropdown", "value"),
               Input("facet-row-dropdown", "value"),
               Input("facet-col-dropdown", "value"),
               Input("sameple-slider", "value"), Input("checklist", "values")],
              [State('facet-grid', 'figure')])
def redrawGraph(x, y, color, row, col, size, checklist, prevLayout):
    df = deepcopy(diamonds[:size])
    df = df.reset_index(drop=True)
    # print(x)
    # print(y)
    # print(row)
    # print(col)
    # print(color)
    rowVal = row
    colVal = col
    if(row == 'None'):
        rowVal = None
    if(col == 'None'):
        colVal = None
    if(color == 'None'):
        color = None
    if('jitter' in checklist):
        df = pd.concat([deepcopy(df), jitter(df, x, y)], ignore_index=True)
        # print(df)
    fig = None
    fig = ff.create_facet_grid(
        df,
        x=x,
        y=y,
        color_name=color,
        facet_row=rowVal,
        facet_col=colVal,
        marker=dict(
            size=4,
            color='#F9B9F2',
            line=dict(
                width=0.3,
                color='black'
            ),
        ),
    )
    if discrete(x):
        relabel(x, fig, 0)
    if discrete(y):
        relabel(y, fig, 1)

    fig['layout']['hovermode'] = 'closest'
    fig['layout']['height'] = 900
    fig['layout']['width'] = None
    if not rowVal and not colVal:
        fig['layout']['yaxis']['zeroline'] = False
        fig['layout']['xaxis']['zeroline'] = False
        fig['layout']['yaxis']['title'] = y
        fig['layout']['annotations'][1]['text'] = ""
        fig['layout']['xaxis']['title'] = x
        fig['layout']['annotations'][0]['text'] = ""
    fig['layout']['autosize'] = True
    return fig


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/af8e469522e38e1a2340e7d32db30b7c34760df8/dash-diamonds-explorer",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})


if __name__ == '__main__':
    app.run_server(debug=True)
