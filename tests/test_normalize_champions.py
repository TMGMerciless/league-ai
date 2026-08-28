import json
from pathlib import Path

from src.normalize_champions import normalize_champion


RAW_DATA_DIR = Path("data/raw")


def get_latest_version_path():
    version_dirs = [
        path for path in RAW_DATA_DIR.iterdir()
        if path.is_dir()
    ]

    return max(
        version_dirs,
        key=lambda path: path.stat().st_mtime
    )


def test_all_champions_normalize():
    version_path = get_latest_version_path()
    champion_files = sorted(
        (version_path / "champions").glob("*.json")
    )

    assert len(champion_files) > 0

    for champion_file in champion_files:
        with champion_file.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)

        champion_id = champion_file.stem
        champion = raw_data["data"][champion_id]

        normalized = normalize_champion(champion)

        assert normalized["id"]
        assert normalized["name"]
        assert normalized["base_stats"]["hp"] > 0
        assert normalized["passive"]["name"]
        assert len(normalized["abilities"]) > 0
