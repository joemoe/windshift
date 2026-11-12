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
