"""Plot a satellite's nadir swath with a time slider, on a plotly globe or in kepler.gl."""
from enum import Enum
from pathlib import Path
from typing import Annotated

import httpx
import numpy as np
import typer
from pyproj import Geod
from skyfield.api import EarthSatellite, load, wgs84

from plot_kepler import plot_kepler
from plot_plotly import plot_plotly


class Backend(str, Enum):
    plotly = "plotly"
    kepler = "kepler"


def compute_swath(tle, swath_km, hours, step_s):
    """Propagate the TLE from now and return time labels, ground track and left/right swath edges."""
    ts = load.timescale()
    text = httpx.get(tle).text if tle.startswith("http") else Path(tle).read_text()
    sat = EarthSatellite(*text.strip().splitlines()[-2:], ts=ts)
    t = ts.utc(*ts.now().utc[:5], np.arange(0, hours * 3600, step_s))

    sub = wgs84.subpoint_of(sat.at(t))
    lat, lon = sub.latitude.degrees, sub.longitude.degrees

    # Swath edges: half the width out to each side, perpendicular to the ground track
    geod = Geod(ellps="WGS84")
    az = geod.inv(lon[:-1], lat[:-1], lon[1:], lat[1:])[0]
    az = np.append(az, az[-1])
    half = np.full_like(lat, swath_km * 500)
    llon, llat, _ = geod.fwd(lon, lat, az - 90, half)
    rlon, rlat, _ = geod.fwd(lon, lat, az + 90, half)

    return t.utc_strftime("%Y-%m-%d %H:%M:%S"), lon, lat, llon, llat, rlon, rlat


def main(
    tle: Annotated[str, typer.Argument(help="TLE file path or URL")],
    swath_km: Annotated[float, typer.Argument(help="Nadir swath width in km")],
    backend: Annotated[Backend, typer.Option(help="Map to plot on")] = Backend.plotly,
    hours: Annotated[float, typer.Option(help="Duration to propagate from now")] = 3,
    step_s: Annotated[int, typer.Option(help="Time step in seconds")] = 60,
):
    """Plot a satellite's nadir swath with a time slider."""
    plot = plot_kepler if backend == Backend.kepler else plot_plotly
    plot(*compute_swath(tle, swath_km, hours, step_s))


if __name__ == "__main__":
    typer.run(main)
