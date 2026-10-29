"""Swath on a plotly globe with a time slider."""
import plotly.graph_objects as go


def plot_plotly(labels, lon, lat, llon, llat, rlon, rlat, center=(13, 65)):
    """Show the ground track and swath on a globe centered on `center` (lon, lat), with a time slider."""
    def footprint(i):
        return go.Scattergeo(lon=[llon[i], lon[i], rlon[i]], lat=[llat[i], lat[i], rlat[i]],
                             mode="lines+markers", line=dict(color="red", width=3), name="Footprint")

    fig = go.Figure(
        data=[
            go.Scattergeo(lon=llon, lat=llat, mode="lines", line=dict(color="orange"), name="Swath edge"),
            go.Scattergeo(lon=rlon, lat=rlat, mode="lines", line=dict(color="orange"), showlegend=False),
            go.Scattergeo(lon=lon, lat=lat, mode="lines", line=dict(color="gray", dash="dot"), name="Ground track"),
            footprint(0),
        ],
        frames=[go.Frame(data=[footprint(i)], traces=[3], name=labels[i]) for i in range(len(lat))],
    )
    fig.update_geos(projection_type="orthographic", projection_rotation=dict(lon=center[0], lat=center[1]),
                    showocean=True, showland=True)
    fig.update_layout(sliders=[dict(steps=[
        dict(label=s, method="animate", args=[[s], dict(mode="immediate", frame=dict(duration=0, redraw=True))])
        for s in labels
    ])])
    fig.show()
