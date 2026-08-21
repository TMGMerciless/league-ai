"""
League AI - Data Dragon ingestion

Retrieves versioned static League of Legends data from Riot's
Data Dragon service and stores the original JSON locally.

Raw data is intentionally preserved before normalization so that
downstream processing can be reproduced and audited.
"""

import json
from pathlib import Path
from urllib.request import urlopen

DDRAGON_BASE = "https://ddragon.leagueoflegends.com"
DATA_DIR = Path("data/raw")


def get_latest_version():
    url = f"{DDRAGON_BASE}/api/versions.json"

    with urlopen(url) as response:
        versions = json.load(response)

    return versions[0]


def download_json(url):
    with urlopen(url) as response:
        return json.load(response)


def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main():
    version = get_latest_version()

    print(f"Detected Data Dragon version: {version}")

    champion_index_url = (
        f"{DDRAGON_BASE}/cdn/{version}/data/en_US/champion.json"
    )

    champion_index = download_json(champion_index_url)

    save_json(
        champion_index,
        DATA_DIR / version / "champion.json"
    )

    print(
        f"Saved {len(champion_index['data'])} champions"
    )


if __name__ == "__main__":
    main()
