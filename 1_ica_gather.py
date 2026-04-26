#### The following script scrapes ICA circuit data from SCE's ArcGIS server (see url). We also utilized tmux to run the script in the background as its total run time is around 3 hours. In case of errors, we also made the script resume-safe (though this was completed in one tmux session). ####

import requests
import json
import logging
import os

# set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", 
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler("ica_fetch.log") # output log file
                    ])
logger = logging.getLogger(__name__)

URL = "https://drpep.sce.com/arcgis_server/rest/services/hosted/ica_layer/featureserver/2/query"
OUTPUT_FILE = "outputs/ica_circuit_segments.geojson"
BATCH_SIZE = 2000

# fetch data function
def fetch_batch(offset):
    response = requests.get(URL, params={
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "true",
        "f": "geojson",
        "resultOffset": offset,
        "resultRecordCount": BATCH_SIZE
    })
    response.raise_for_status()
    return response.json().get("features", [])

# resume function
def load_existing():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        features = data.get("features", [])
        logger.info(f"Resuming from {len(features)} existing features")
        return features
    return []

# in case of error, save function saves collected features
def save(features):
    with open(OUTPUT_FILE, "w") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f)

# MAIN LOOP
def main():
    all_features = load_existing()
    offset = len(all_features)

    while True:
        logger.info(f"Fetching offset {offset}...")
        batch = fetch_batch(offset)
        if not batch:
            break
        all_features.extend(batch)
        save(all_features)
        logger.info(f"Saved {len(all_features)} features total")
        offset += BATCH_SIZE

    logger.info(f"Done — {len(all_features)} total features")

if __name__ == "__main__":
    main()