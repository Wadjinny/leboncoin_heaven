# %%
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from ast import literal_eval as ast
import numpy as np
import plotly.graph_objects as go
from rich import print
from datetime import datetime


offers_df = pd.read_json("offers_v2.json", convert_dates=["first_publication_date"])
type_to_not_keep = ["Parking", "Autre"]
offers_df = offers_df[~offers_df["real_estate_type"].isin(type_to_not_keep)]
# offers_df = offers_df[offers_df["price"] < 650]
work_pos = (44.861252, -0.552376)
offers_df["distance"] = offers_df.apply(
    lambda x: np.linalg.norm([x["lat"] - work_pos[0], x["lng"] - work_pos[1]], ord=2),
    axis=1,
)
"""
    ['price', 'subject', 'first_publication_date', 'status', 'body',
       'has_phone', 'url', 'lat', 'lng', 'city', 'images', 'charges_included',
       'district_id', 'district_resolution_type', 'district_type_id',
       'district_visibility', 'elevator', 'owner', 'energy_rate', 'floor_number',
       'furnished', 'ges', 'is_import', 'lease_type', 'nb_floors_building',
       'nb_parkings', 'old_price', 'outside_access', 'profile_picture_url',
       'rating_count', 'rating_score', 'real_estate_type', 'rooms', 'square',
       'corrected_price', 'distance']
"""
# %%
fig = px.scatter_mapbox(
    offers_df,
    lat="lat",
    lon="lng",
    zoom=12,
    mapbox_style="carto-positron",
    hover_name="subject",
    hover_data=["price"],
)
fig.update_layout(
    dragmode="lasso",
)
fig.add_trace(
    go.Scattermapbox(
        lat=[work_pos[0]],
        lon=[work_pos[1]],
        mode="markers",
        marker=dict(size=20, color="red"),
        text=["Work location"],
        showlegend=False,
    )
)
fig.update_traces(
    marker=dict(size=10),
)
fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    mapbox_style="open-street-map",
)
fig_view = dcc.Graph(figure=fig, id="fig")
info_selected_point = html.Div(id="more-data-view", children="More data here")
selected_points = html.Div(id="selected-points", children="Selected points here")

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1(
            children=f"Leboncoin Search {len(offers_df)} offer",
            style={"textAlign": "center"},
        ),
        fig_view,
        selected_points,
        info_selected_point,
    ]
)


@callback(Output("more-data-view", "children"), Input("fig", "clickData"))
def update_more_data_view(click_data):
    if click_data is None:
        return "more data here"
    else:
        id = click_data["points"][0]["pointIndex"]
        more_info = offers_df.iloc[id]
        more_info = more_info.to_dict()
        more_info = {k: v for k, v in more_info.items() if v is not None}
        more_info["url"] = html.A(
            more_info["url"], href=more_info["url"], target="_blank"
        )
        more_info["location"] = f"{more_info['lat']}, {more_info['lng']}"

        if "images" in more_info.keys() and not isinstance(more_info["images"], float):
            more_info["images"] = [html.Img(src=img) for img in more_info["images"]]
        if "profile_picture_url" in more_info.keys():
            more_info["profile_picture_url"] = html.Img(
                src=more_info["profile_picture_url"]
            )
        return html.Div(
            [
                html.H2("More data"),
                html.Table(
                    [html.Tr([html.Td(k), html.Td(v)]) for k, v in more_info.items()]
                ),
            ]
        )
        return "point clicked"


@callback(
    Output("selected-points", "children"),
    Input("fig", "selectedData"),
)
def group_point_selected(selected_points):
    if selected_points is None:
        return "Selected points here"
    points = [point["pointIndex"] for point in selected_points["points"]]
    selected_points = offers_df.iloc[points].sort_values("distance")

    list_divs = [html.H2(f"{len(selected_points)} selected points")]
    for i, row in selected_points.iterrows():
        div = html.A(
            html.Div(
                [
                    html.H3(row["subject"], style={"margin": "0"}),
                    html.H4(
                        f"il y a {(datetime.now() - row['first_publication_date']).days} jours",
                        style={"color": "black", "margin": "0"},
                    ),
                    html.Label(f"{row['price']} €"),
                    html.P(f"{row['lat']}, {row['lng']}"),
                    html.Label(
                        f"{row['square']}",
                        style={"padding-left": "10px"},
                    ),
                    html.Label(
                        f"Owner: {row['owner']}",
                        style={
                            "padding-left": "10px",
                            "color": "red" if row["owner"] == "pro" else "green",
                        },
                    ),
                    html.Label(
                        f"Has telephone" if row["has_phone"] else "",
                        style={
                            "padding-left": "10px",
                            "color": "green" if row["has_phone"] else "",
                        },
                    ),
                    html.Label(
                        f"Meuble" if row["furnished"] == "Meublé" else "",
                        style={"color": "yellow"},
                    ),
                ],
                style={"border": "1px solid black", "padding": "10px"},
            ),
            href=row["url"],
            target="_blank",
        )
        list_divs.append(div)
    return list_divs


if __name__ == "__main__":
    app.run(debug=True)
