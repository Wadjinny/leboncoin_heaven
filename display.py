# %%
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from ast import literal_eval as ast
import numpy as np

offers_df = pd.read_csv("offers_v1.csv")
type_to_not_keep = ["Parking", "Autre"]
offers_df = offers_df[~offers_df["real_estate_type"].isin(type_to_not_keep)]
# %%
fig = px.scatter_mapbox(
    offers_df,
    lat="lat",
    lon="lng",
    color="corrected_price",
    # size="price",
    color_continuous_scale=px.colors.sequential.Viridis,
    size_max=15,
    zoom=10,
    mapbox_style="carto-positron",
    hover_name="subject",
    hover_data=["price"],
)
# change the size of all the points
fig.update_traces(marker=dict(size=10))
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_layout(mapbox_style="open-street-map")
fig_view = dcc.Graph(figure=fig, id="fig")

more_data_view = html.Div(id="more-data-view", children="More data here")

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1(children="Fuck Leboncoin", style={"textAlign": "center"}),
        fig_view,
        more_data_view,
    ]
)


@callback(Output("more-data-view", "children"), Input("fig", "clickData"))
def update_more_data_view(click_data):
    if click_data is None:
        return "No data"
    else:
        id = click_data["points"][0]["pointIndex"]
        more_info = offers_df.iloc[id]
        more_info = more_info.to_dict()
        more_info = {k: v for k, v in more_info.items() if v is not None}
        more_info["url"] = html.A(more_info["url"], href=more_info["url"])

        if "images" in more_info.keys() and not isinstance(more_info["images"], float):
            more_info["images"] = [
                html.Img(src=img) for img in ast(more_info["images"])
            ]
        return html.Div(
            [
                html.H2("More data"),
                html.Table(
                    [html.Tr([html.Td(k), html.Td(v)]) for k, v in more_info.items()]
                ),
            ]
        )
        # return f"More data here: {click_data}"


if __name__ == "__main__":
    app.run(debug=True)
