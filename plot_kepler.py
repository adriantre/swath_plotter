"""Swath in kepler.gl with the time filter shown."""
import webbrowser
from pathlib import Path

import geopandas as gpd
import numpy as np
from keplergl import KeplerGl
from shapely.geometry import Polygon


def plot_kepler(labels, lon, lat, llon, llat, rlon, rlat, center=(13, 65)):
    """Open the swath in kepler.gl centered on `center` (lon, lat), with the time filter shown."""
    # One quad per time step. Longitudes are kept within 180° of the first corner, so a quad crossing
    # the antimeridian is drawn whole, extending past ±180, instead of stretching across the map.
    quads = []
    for i in range(len(labels) - 1):
        x = np.array([llon[i], rlon[i], rlon[i + 1], llon[i + 1]])
        x = x[0] + (x - x[0] + 180) % 360 - 180
        quads.append(Polygon(zip(x, [llat[i], rlat[i], rlat[i + 1], llat[i + 1]])))
    gdf = gpd.GeoDataFrame({"time": labels[:-1]}, geometry=quads, crs=4326)
    config = {"version": "v1", "config": {
        "visState": {"filters": [{"dataId": ["swath"], "id": "time", "name": ["time"],
                                  "type": "timeRange", "enlarged": True}]},
        "mapState": {"longitude": center[0], "latitude": center[1], "zoom": 3},
    }}
    html = Path("swath.html")
    KeplerGl(data={"swath": gdf}, config=config).save_to_html(file_name=str(html))
    # The exported map only sizes itself to the window on a resize event, so fire one on load
    resize = "<script>window.addEventListener('load', () => window.dispatchEvent(new Event('resize')))</script>"
    head, _, tail = html.read_text().rpartition("</body>")
    html.write_text(head + resize + "</body>" + tail)
    webbrowser.open(html.resolve().as_uri())
