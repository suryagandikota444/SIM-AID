# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import io
import os
import base64
from dash import Dash, html, dcc, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import pickle
from umap import UMAP
from sklearn.cluster import DBSCAN
from PIL import Image

external_script = ["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]

app = Dash(
    __name__,
    external_scripts=external_script,
)
app.scripts.config.serve_locally = True

with open('/Users/sachinchanchani/Desktop/dash-th2023/data3d.pkl', 'rb') as p:
    data = pickle.load(p)
del data["UMAP"]
del data["representation"]
del data["DBSCAN"]
data['label'] == [str(l) for l in data['label']]
data['path'] = ['/Users/sachinchanchani/Desktop/dash-th2023/data' + str(loc.strip().split('tiles_5000')[-1]) for loc in data['path']]
df = pd.DataFrame.from_dict(data)

fig = px.scatter_3d(df, x='x', y='y', z='z', color='label')
fig.update_traces(marker_size=2.5, hoverinfo="none", hovertemplate=None)
fig.update_layout(clickmode='event+select', margin=dict(l=0, r=0, b=20, t=0))

# Initialize a dictionary to store the descriptions of each unique value in 'cluster'
cluster_descriptions = {}
for c in set(data['cluster']):
    cluster_descriptions[c] = ''

label2string = {
    0: "TUMOR",
    1: "STROMA",
    2: "COMPLEX",
    3: "LYMPHO",
    4: "DEBRIS",
    5: "MUCOSA",
    6: "ADIPOSE",
    7: "EMPTY",
}

app.layout = html.Div(
    className="",
    children=[
        html.Div(
            className="row justify-center flex",
            children=[
                html.Div(
                    className="col-lg-12 font-bold text-3xl border-b-2 w-full text-center",
                    children=[
                        html.Div("5,000 histological images of human colorectal cancer and healthy tissue", id="title",
                        className="my-10 ml-2"
                        ),
                    ]
                )
            ]
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    style={"display": "flex", "flex-direction": "row", "align-items": "center", "justify-content": "center"},
                    children=[
                        dcc.RadioItems(
                            id="color-picker",
                            style={"padding": "20px"},
                            className="space-x-2 flex flex-col justify-left",
                            options=[
                                {"label": " Cluster", "value": "cluster"},
                                {"label": " Label", "value": "label"},
                            ],
                            value="cluster",
                        ),
                        html.Div(
                            style={"justify-content": "center", "padding": "20px"},
                            children=[
                                html.Div(
                                    style={"margin-bottom": "10px"},
                                    children=[
                                        dcc.Input(id="cluster_input", style={"width": "300px", "height": "125px"}, type="text", value="", placeholder="Type observations here.", className="border border-black rounded shadow-lg"),
                                    ],
                                ),
                                html.P("Comments on group: ", id='cluster-prompt', className="text-gray-500")
                            ],
                        ),
                    ],
                ),
                
                html.Div(
                    className="w-full",
                    children=[
                        html.Div([
                            # The graph
                            dcc.Graph(
                                id="3d-scatter-plot",
                                figure=fig,
                                style={"height": "80%", "width": "80%", "display": "flex"},
                                className="w-full px-14"
                            ),
                            dcc.Tooltip(id="graph-tooltip-5", direction='bottom')
                            ],
                            id="plot-div",
                            className="eight columns ",
                        ),
                    ]
                ),
            ]
        )
    ]
)

@app.callback(
    Output(component_id='3d-scatter-plot', component_property='figure'),
    [Input(component_id='color-picker', component_property='value')]
)
def update_scatter_plot(color_by):
    g = px.scatter_3d(df, x='x', y='y', z='z', color=color_by)
    g.update_layout(clickmode='event+select', margin=dict(l=0, r=0, b=0, t=0))
    g.update_traces(marker_size=2.5, hoverinfo="none", hovertemplate=None)
    return g

@app.callback(
    Output('cluster-prompt', 'children'),
    [Input('3d-scatter-plot', "clickData"), Input("cluster_input", 'value')])
def update_annotation_prompt(clickData, annotation):
    if clickData is None:
        raise PreventUpdate

    cluster = str(clickData['points'][0]['marker.color'])
    cluster_descriptions[cluster] = annotation
    return "Comments on group " + str(clickData['points'][0]['marker.color'])

def np_image_to_base64(path_to_tif):
    im = Image.open(path_to_tif)
    buffer = io.BytesIO()
    im.save(buffer, format="jpeg")
    encoded_image = base64.b64encode(buffer.getvalue()).decode()
    im_url = "data:image/jpeg;base64, " + encoded_image
    return im_url

@app.callback(
    Output("graph-tooltip-5", "show"),
    Output("graph-tooltip-5", "bbox"),
    Output("graph-tooltip-5", "children"),
    Input("3d-scatter-plot", "hoverData"),
)
def display_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update

    # demo only shows the first point, but other points may also be available
    hover_data = hoverData["points"][0]
    bbox = hover_data["bbox"]
    num = hover_data["pointNumber"]

    im_url = np_image_to_base64(data['path'][num])
    children = [
        html.Div([
            html.Img(
                src=im_url,
                style={"width": "150px", 'display': 'block', 'margin': '0 auto'},
            ),
            html.P("Tissue Scan" + str(label2string[data['label'][num]]), style={'font-weight': 'bold'})
        ])
    ]

    return True, bbox, children

if __name__ == '__main__':
    app.run_server(debug=True)

