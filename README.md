# SCE Data Gathering

This repository contains the methods that our team implemented to compile Integration Capacity Analysis (ICA) data from one of California's Investor Owned Utilities, Southern California Edison (SCE).

## About

Upon initial exploration, our team downloaded ICA data from SCE off of their [public ArcGIS Hub](https://drpep-sce2.opendata.arcgis.com/maps/23f48820904b46c38f0d4f2d75c69d23/about), specifically the `ICA - Circuit Segments` layer within the ICA Layer. After further investigation, the downloaded data seemed to be missing ~100k entries when comparing what was displayed on the online interactive portal. To gather the full data, we built a Python script to query the `ICA - Circuit Segments` layer in the ArcGIS FeatureServer.


## Contents

1. **1_ica_gather.py**: Querying script to gather data from SCE's DRPEP ArcGIS FeatureServer to retrieve all ICA Circuit Segment features (Layer 2) as GeoJSON. Fetches entries in batches of 2,000 records and saves incrementally to `outputs/ica_circuit_segments.geojson`, creating `outputs` folder if not already existing. The script supports resuming upon session interruption and progress is logged to `ica_fetch.log`.

2. **2_ica_fetch.log**: The resulting log from running the query script.

3. **3_view_data.ipynb**: Investigative notebook to confirm and explore the queried data.
