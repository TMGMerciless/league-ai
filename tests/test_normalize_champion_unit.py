import os
import pytest

from src.normalize_champions import (
    get_latest_local_version,
    normalize_champion,
)


@pytest.fixture
def sample_champion():
    return {
        "id": "TestChampion",
        "name": "Test Champion",
        "tags": ["Fighter"],
        "partype": "Mana",
        "info": {
            "attack": 7,
            "defense": 5,
            "magic": 3,
            "difficulty": 4,
        },
        "stats": {
            "hp": 600,
            "hpperlevel": 100,
            "mp": 300,
            "mpperlevel": 50,
            "movespeed": 340,
            "armor": 35,
            "armorperlevel": 4,
            "spellblock": 32,
            "spellblockperlevel": 2,
            "attackrange": 175,
            "hpregen": 6,
            "hpregenperlevel": 0.7,
            "mpregen": 8,
            "mpregenperlevel": 0.8,
            "crit": 0,
            "critperlevel": 0,
            "attackdamage": 62,
            "attackdamageperlevel": 3,
            "attackspeedperlevel": 2.5,
            "attackspeed": 0.65,
        },
                "passive": {
            "name": "Test Passive",
            "description": "A synthetic passive used for unit testing.",
        },
        "spells": [
            {
                "id": "TestQ",
                "name": "Test Ability",
                "description": "A synthetic ability used for unit testing.",
                "tooltip": "Deals test damage.",
                "maxrank": 5,
                "cooldown": [10, 9, 8, 7, 6],
                "cost": [40, 45, 50, 55, 60],
                "costType": "Mana",
                "range": [600, 600, 600, 600, 600],
            }
        ],
    }

def test_normalize_champion(sample_champion):
    normalized = normalize_champion(sample_champion, "16.16.1")

    assert normalized["patch_version"] == "16.16.1"
    assert normalized["id"] == "TestChampion"
    assert normalized["name"] == "Test Champion"
    assert normalized["resource_type"] == "Mana"

    assert normalized["base_stats"]["hp"] == 600
    assert normalized["base_stats"]["resource"] == 300
    assert normalized["base_stats"]["attack_range"] == 175

    assert normalized["passive"]["name"] == "Test Passive"

    assert len(normalized["abilities"]) == 1
    assert normalized["abilities"][0]["spell_id"] == "TestQ"
    assert normalized["abilities"][0]["cooldowns"] == [10, 9, 8, 7, 6]

def test_get_latest_local_version_uses_patch_number(tmp_path, monkeypatch):
    older = tmp_path / "16.16.1"
    newer = tmp_path / "16.17.1"

    older.mkdir()
    newer.mkdir()

    os.utime(newer, (1000, 1000))
    os.utime(older, (2000, 2000))

    monkeypatch.setattr(
        "src.normalize_champions.RAW_DATA_DIR",
        tmp_path,
    )

    latest = get_latest_local_version()

    assert latest.name == "16.17.1"
