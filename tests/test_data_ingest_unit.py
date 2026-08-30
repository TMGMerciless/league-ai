import json

from src.data_ingest import version_is_complete


def test_version_is_complete_returns_true_when_all_files_exist(
    tmp_path,
    monkeypatch,
):
    version = "16.17.1"
    version_dir = tmp_path / version
    champions_dir = version_dir / "champions"

    champions_dir.mkdir(parents=True)

    champion_index = {
        "data": {
            "Aatrox": {},
            "Ahri": {},
        }
    }

    with (version_dir / "champion.json").open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(champion_index, file)

    for champion_id in champion_index["data"]:
        with (champions_dir / f"{champion_id}.json").open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump({}, file)

    monkeypatch.setattr(
        "src.data_ingest.DATA_DIR",
        tmp_path,
    )

    assert version_is_complete(version) is True

def test_version_is_complete_returns_false_when_champion_is_missing(
    tmp_path,
    monkeypatch,
):
    version = "16.17.1"
    version_dir = tmp_path / version
    champions_dir = version_dir / "champions"

    champions_dir.mkdir(parents=True)

    champion_index = {
        "data": {
            "Aatrox": {},
            "Ahri": {},
        }
    }

    with (version_dir / "champion.json").open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(champion_index, file)

    with (champions_dir / "Aatrox.json").open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump({}, file)

    monkeypatch.setattr(
        "src.data_ingest.DATA_DIR",
        tmp_path,
    )

    assert version_is_complete(version) is False
