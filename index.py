import dash
from dash import dcc
from dash import html
from api.data_cleaning import cleanScanData
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import datetime

app = dash.Dash(__name__, external_stylesheets=["./style.css"], meta_tags=[{"name": "viewport", "content": "width=device-width"}])

df_scanlog, \
tech_table, \
df_monthlyJobsDiscrepancies, \
df_pieChart, \
days_without_discrepancies = cleanScanData()


app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # in milliseconds
        n_intervals=0
    ),
    html.Div(id='dynamic-content'),
])

@app.callback(Output('dynamic-content', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_dynamic_content(n):
        df_scanlog, tech_table, df_monthlyJobsDiscrepancies, df_pieChart, days_without_discrepancies = cleanScanData()
        return [
            html.Div(id="mainContainer",
                style={"display": "flex", "flex-direction": "column"}, children=[ 
                html.Div([
                    html.Div([
                        html.Img(src=app.get_asset_url('logo.svg'),
                                 id='logo-image',
                                 style={
                                     "height": "60px",
                                     "width": "auto",
                                     "margin-bottom": "0px",
                                 },
                                )
                    ],
                        className="one-third column",
                    ),
                    html.Div([
                        html.Div([
                            html.H3("Technician Overview", style={"margin-bottom": "0px", 'color': 'white'}),
                            html.H5("Track Activity", style={"margin-top": "0px", 'color': 'white'}),
                        ])
                    ], className="one-half column", id="title"),

                    html.Div([
                        html.H6("Last Updated: {}".format(datetime.datetime.now())),

                    ], className="one-third column", id='title1'),

                ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),
                #Cards
                html.Div([
                    html.Div([
                        html.Img(src=app.get_asset_url('box-solid.svg'), className='card-icons'), 
                        html.H6(children='Orders',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white',
                                    'fontSize': 30}
                                ),
                                html.P(id='total-orders',
                                    children=df_scanlog["refCode"].nunique(),
                                style={
                                   'textAlign': 'center',
                                   'color': 'white',
                                   'fontSize': 40}
                               ),
                        ], className="card_container three columns",
                    ),

                    html.Div([
                        html.Img(src=app.get_asset_url('barcode-solid.svg'), className='card-icons'),
                        html.H6(children='Total Scans',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white',
                                    'fontSize': 30}
                                ),
                                html.P(id="total-scans",
                                    children=len(df_scanlog["barcode"]),
                                style={
                                   'textAlign': 'center',
                                   'color': 'white',
                                   'fontSize': 40}
                               ),
                        ], className="card_container three columns",
                    ),
                    html.Div([
                        html.Img(src=app.get_asset_url('calendar-days-solid.svg'), className='card-icons'),
                        html.H6(children='Days Without Errors',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white',
                                    'fontSize': 30}
                                ),
                                html.P(id="days-without-discrepancies",
                                    children=(days_without_discrepancies),
                                style={
                                   'textAlign': 'center',
                                   'color': '#06d6a0',
                                   'fontSize': 40}       
                                       ),

                            ], className="card_container three columns",
                    ),

                    html.Div([
                        html.Img(src=app.get_asset_url('xmark-solid.svg'), className='card-icons'),
                        html.H6(children='Errors',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white',
                                    'fontSize': 30}
                                ),
                                html.P(id="total-erros",
                                    children=(df_monthlyJobsDiscrepancies['Discrepancies'].sum()),
                                style={
                                   'textAlign': 'center',
                                   'color': '#e63946',
                                   'fontSize': 40}       
                                       ),
                            ], className="card_container three columns")

                ], className="row flex-display"), #end of Cards

                # Tech table, pie chart, bar chart
                html.Div(className="row flex-display", children=[
                        html.Div(className="create_container four columns", children=[
                                dcc.Graph(id='pie_chart', style={'height': '100%', 'width': '100%'},
                                    figure={
                                        "data": [
                                    {
                                        "values": (df_pieChart['count']),
                                        "labels": (df_pieChart['Discrepancies']),
                                        "type": "pie",
                                        "hole": 0.4, 
                                        "marker": {"colors": ["#ffbe0b", "#fb5607", "#ff006e", "#8338ec", "#669bbc", "#3a86ff", "#e63946"]},
                                        "textinfo": "percent+labels",
                                        "textposition": "inside",
                                    }
                                        ],
                                    "layout": {
                                        "title": "Errors Breakdown",
                                        "font": {"color": "#ffffff", "size": 20},
                                        "plot_bgcolor": "#191C24",
                                        "paper_bgcolor": "#191C24",
                                        'margin': {'t': 50, 'r': 20, 'b': 20, 'l': 20} 
                                        },
                                    },
                                ),
                            ]
                        ),
                        html.Div(className="create_container four columns", children=[
                            dcc.Graph(id="bar-chart2",
                                figure={
                                    "data": [
                                    {
                                      "x": tech_table['Orders'],
                                      "y": tech_table['Technician'],
                                      "name": "Orders",
                                      "type": "bar",
                                      "marker": {"color": "#0d6efd"},
                                      "text": tech_table['Orders'], 
                                      "textposition": "inside", 
                                      "textfont": {"color": "#ffffff", "size": 25},
                                      "orientation":"h"
                                    },
                                    {
                                      "x": tech_table['Discrepancies'],
                                      "y": tech_table['Technician'],
                                      "name": "Errors",
                                      "type": "bar",
                                      "marker": {"color": "orange"},
                                      "text": tech_table['Discrepancies'],
                                      "textposition": "inside",  
                                      "font": {"color": "#ffffff", "size": 25},
                                      "orientation":"h" 
                                    },
                                    {
                                      "x": tech_table["+Feedback"],
                                      "y": tech_table['Technician'],
                                      "name": "Positive Feedback",
                                      "type": "bar",
                                      "text": tech_table["+Feedback"],
                                      "textposition": "inside",  
                                      "font": {"color": "#ffffff", "size": 25},
                                      "marker": {"color": "#06d6a0"},
                                      "orientation":"h" 
                                    }
                                        ],
                                    "layout": {
                                      "title": "Technicians",
                                      "plot_bgcolor": "#191C24",
                                      "paper_bgcolor": "#191C24",
                                      "barmode": "stack",
                                      "font": {"color": "#ffffff", "size": 20},
                                      'margin': {'t': 50, 'r': 20, 'b': 30, 'l': 100},
                                      "xaxis": {"tickfont": {"size": 14}}      
                                    },
                                }
                            )        
                        ]),
                        html.Div(className="create_container four columns", children=[
                            dcc.Graph(id="bar-chart",
                                      figure={
                                          "data": [
                                            {
                                                "x": df_monthlyJobsDiscrepancies['month'],
                                                "y": df_monthlyJobsDiscrepancies['refCode'],
                                                "name": "Orders",
                                                "type": "bar",
                                                "marker": {"color": "#0d6efd"},
                                                "text": df_monthlyJobsDiscrepancies['refCode'], 
                                                "textposition": "inside", 
                                                "textfont": {"color": "#ffffff", "size": 20}
                                            },
                                            {
                                                "x": df_monthlyJobsDiscrepancies['month'],
                                                "y": df_monthlyJobsDiscrepancies['Discrepancies'],
                                                "name": "Errors",
                                                "type": "bar",
                                                "marker": {"color": "orange"},
                                                "text": df_monthlyJobsDiscrepancies['Discrepancies'],
                                                "textposition": "inside",  
                                                "textfont": {"color": "#ffffff"} 
                                            },
                                            ],
                                          "layout": {
                                                "title": "Orders by Month",
                                                "plot_bgcolor": "#191C24",
                                                "paper_bgcolor": "#191C24",
                                                "barmode": "stack",
                                                "font": {"color": "#ffffff", "size": 20},
                                                'margin': {'t': 50, 'r': 35, 'b': 30, 'l': 40}               
                                            },
                                        }
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            )
        ]

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)