# swath-viewer

This tool plots a satellite's nadir swath over time, either on a plotly globe or in kepler.gl, with a time slider.

![Sentinel-2B swath on the plotly globe](docs/plotly_globe.gif)

## Install

The project is managed with [uv](https://docs.astral.sh/uv/), a fast Python package and project manager that
installs Python itself, creates the virtual environment and keeps dependencies in sync with `uv.lock`.

```bash
# Install uv. You can also install it with brew install uv.
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create .venv with Python 3.12 and the locked dependencies.
cd swath_viewer
uv sync
```

`uv run` also syncs the environment, so running the command below works without the `uv sync` step.

## Input

The first input is a file path or URL to a two-line element set (TLE). A name line above the two TLE lines is
fine, so CelesTrak's `FORMAT=TLE` output works as is. The file [`examples/sentinel2b.tle`](examples/sentinel2b.tle)
is an example.

```
SENTINEL-2B
1 42063U 17013A   26301.63409036  .00000235  00000+0  10633-3 0  9995
2 42063  98.5738  14.4995 0001101  89.7594 270.3715 14.30816928503728
```

A TLE goes stale as the orbit drifts. For accurate positions, fetch a fresh one from
`https://celestrak.org/NORAD/elements/gp.php?CATNR=42063&FORMAT=TLE`.

The second input is the swath width, which is the full nadir footprint width in km. The swath is drawn half that
width out to each side of the ground track.

The orbit is propagated from the current time, for `--hours` hours in steps of `--step-s` seconds.

## Usage

```bash
uv run plot_swath.py <tle_file_or_url> <swath_km> [--backend plotly|kepler] [--hours 3] [--step-s 60]
```

The examples below plot Sentinel-2B with its 290 km swath.

```bash
# Plot the swath on a plotly globe.
uv run plot_swath.py examples/sentinel2b.tle 290

# Plot the swath in kepler.gl for 1 hour from now.
uv run plot_swath.py examples/sentinel2b.tle 290 --backend kepler --hours 1

# Fetch the latest TLE straight from CelesTrak.
uv run plot_swath.py "https://celestrak.org/NORAD/elements/gp.php?CATNR=42063&FORMAT=TLE" 290
```

The plotly backend opens an orthographic globe in the browser. The slider moves the current footprint along the
swath.

The kepler backend writes `swath.html` to the current directory and opens it. The time filter is shown at the
bottom. Drag its window or press play to sweep the swath.

Both maps open centred on Norway.
