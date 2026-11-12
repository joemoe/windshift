# Windshift – live wind for eastern Lake Constance

A single-page prototype that shows current wind conditions in the eastern part of Lake Constance (Bodensee), built entirely on open data and fetched live in the browser.

## Stations

| Station | Provider | Data |
|---|---|---|
| Lindau | DWD (via [Bright Sky](https://brightsky.dev)) | current 10-min values |
| Bregenz | [GeoSphere Austria](https://data.hub.geosphere.at/dataset/tawes-v1-10min), TAWES 11101 | 10-min values, last 3 h |
| Rohrspitz | GeoSphere Austria, TAWES 11299 | 10-min values, last 3 h |
| Altenrhein | [MeteoSwiss Open Data](https://opendatadocs.meteoswiss.ch/a-data-groundbased/a1-automatic-weather-stations), ARH | 10-min values, last 3 h |

Map tiles: Esri World Dark Gray Base, © OpenStreetMap contributors. Map library: [Leaflet](https://leafletjs.com).

## Run

No build step. Open `index.html` in a browser or serve it from any static host (this repo is set up for GitHub Pages).

## Disclaimer

Prototype only – not an official storm warning. Always follow the official storm warning lights around the lake.

## Wind-system model

The animated flow is not an interpolation but a conceptual model of eight local wind systems that shape the eastern lake. Each has an assumed spatial shape and a strength:

| System | Assumption |
|---|---|
| Westerly (large-scale) | Channelled along the lake axis, slowed and split by the Pfänder/Alps wall at the eastern end |
| Northerly / Bise | NE down the lake, bending into the Rhine Valley near the south shore, Bregenz bay partly in the Pfänder lee |
| Rhine Valley | Föhn / mountain wind leaving the valley over the delta (positive) or daytime valley breeze into it (negative) |
| Rhine river outflow | Narrow cold-air jet out of the new Rhine mouth |
| Bregenzerwald / Bregenzer Ach | SE gap/drainage wind incl. the south-east Pfänderwind over the Gebhardsberg |
| Pfänder downslope wind | Classical E/NE Pfänderwind falling onto Lochau and Bregenz |
| Swiss hills (Appenzell) | S/SSW downslope wind onto Rorschach–Altenrhein |
| Thermal | Night land breeze converging over the lake (positive) or afternoon lake breeze (negative) |

- **Live mode** fits the strengths to the four stations (bounded, ridge-regularised least squares) and blends the remaining differences in near each station.
- **Simulator mode** lets you set each system or load a scenario.
- **Boat**: drop a boat that holds a fixed angle to the wind (sails never touched) and watch its track. In the "Calm night" scenario the land-breeze convergence makes it sail a full circle.

Sources for the assumptions: Gohm, Siller & Bär (2015), *Nature and climatology of Pfänderwind*, Meteorol. Z. 24(3); MeteoSwiss/SRF on Rhine Valley föhn reaching Rorschach–Altenrhein; DWD on the land–lake breeze at Friedrichshafen; ZAMG/vol.at report of a "mini convergence" over the eastern lake.
