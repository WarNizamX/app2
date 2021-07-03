#!/usr/bin/env python
# coding: utf-8

# In[1]:



import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd

df = pd.read_csv('Fire_IncidentsMalaysia1.csv')

# Themes
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA]) # https://bootswatch.com/default/

# Modal Button
modal = html.Div(
    [
        dbc.Button("Click me!! For More Info about the Dropdown", id="open",color="info",style={'font-size': '15px',
                                                                                               'font-weight': 'bold',}),    
        html.Br(),
        html.Br(),
        
        dbc.Modal([
            dbc.ModalHeader("Information about dropdown"),
            dbc.ModalBody(
                
                html.H6("You can type,search inside the dropdown and click 'X' to dismissed current visualization", 
                        className="card-text",
                         style={'font-size': '30px','font-weight': 'bold', 'margin': '0 10px 0 10px'}),
                
            ),
            dbc.ModalFooter(
                dbc.Button("Close", id="close", className="ml-auto")
            ),

        ],
            id="modal",
            is_open=False,    # True, False
            size="xl",        # "sm", "lg", "xl"
            backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
            scrollable=True,  # False or True if modal has a lot of text
            centered=True,    # True, False
            fade=True         # True, False
        ),
    ]
)

# Alert Button
alert = dbc.Alert("Please choose Type of Fire from dropdown to avoid further disappointment!",style={'font-size': '20px'},
                  color="danger",dismissable=True),  # use dismissable or duration=5000 for alert to close in x milliseconds

image_card = dbc.Card(
    [
        dbc.CardBody(
            [
                
                dbc.CardImg(src="/assets/types.png", title="Fire"),
                html.H6("Choose Type of Fire:", className="card-text",style={'font-size': '25px','font-weight': 'bold'}),
                html.Div(id="the_alert", children=[]),
                
                # Dropdown Button
                dcc.Dropdown(id='district_chosen', options=[{'label': d, "value": d} for d in df["Type of Fire"].unique()],
                             value=["Building", "Bushes", "Others","Vehicles","Trash"], multi=True, style={"color": "#000000"}),
                html.Hr(),
                modal
            ]
        ),
        
    ],
    style={"width": "70rvh",'height': '70rvh'},color="secondary",
)

graph_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Hover to the graph to see the data and click  'About Fire Type Graph'  for more info", 
                        className="card-title", style={"text-align": "center",'font-weight': 'bold'}),
                dbc.Button(
                    "About Type of Fire Graph", id="popover-bottom-target", color="info",style={'font-size': '18px',
                                                                                               'font-weight': 'bold'}
                ),
                # Pop Over Button
                dbc.Popover(
                    [
                        dbc.PopoverHeader("The 'Others' types of fire cases can be identified as Bullet Bunker,"
" Electrical Substations,Generator, Signboard, Dam and Electricity Poles",style={'font-size': '25px','font-weight': 'bold'}),
                        dbc.PopoverBody(
                            "P/S: ",style={'font-size': '20px'}),
                    ],
                    id="popover",
                    target="popover-bottom-target",  # needs to be the same as dbc.Button id
                    placement="bottom",
                    is_open=False,
                ),
                dcc.Graph(id='line_chart', figure={},
                         style={'height':'85vh', "width" : "100%"}),

            ]
        ),
    ],
    color="secondary",
)

# *********************************************************************************************************
app.layout = html.Div([
    dbc.Row([dbc.Col(image_card, width=4), dbc.Col(graph_card, width=8)], justify="around")
])
# *********************************************************************************************************

@app.callback(
    Output("popover", "is_open"),
    [Input("popover-bottom-target", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    [Output("line_chart", "figure"),
     Output("the_alert", "children")],
    [Input("district_chosen", "value")]
)
def update_graph_card(districts):
    if len(districts) == 0:
        return dash.no_update, alert
    else:
        df_filtered = df[df["Type of Fire"].isin(districts)]
        df_filtered = df_filtered.groupby(["Year", "Type of Fire"])[['Number of Cases']].sum().reset_index()
        fig = px.line(df_filtered, x="Year", y="Number of Cases", color="Type of Fire",template='ggplot2',
                      labels={"<b>Number of Cases": "Number of Fire Cases<b>"}).update_traces(mode='lines+markers')
       
        fig.update_layout(
            margin=dict(t=95, b=0, l=0, r=0),
            title={
            'text': "<b>Type of Fire in Malaysia: 2015 to 2020",
            'x':0.5,

            'xanchor': 'center',
            'yanchor': 'top'},
            xaxis_title="Year",
            yaxis_title="Number of Fire Cases",
            legend_title="Type of Fire Cases",
            font=dict(
            family="san serif",
            size=30,
            color="black"
        )
    )
    return fig, dash.no_update

@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=False, port=8058)


# In[ ]:





# In[ ]:




