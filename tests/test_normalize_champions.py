import pytest
import json
from pathlib import Path

from src.normalize_champions import normalize_champion


RAW_DATA_DIR = Path("data/raw")

if not RAW_DATA_DIR.exists():
    pytest.skip(
        "Riot Data Dragon data not available",
        allow_module_level=True,
    )

def get_latest_version_path():
    version_dirs = [
        path for path in RAW_DATA_DIR.iterdir()
        if path.is_dir()
    ]

    return max(
        version_dirs,
        key=lambda path: path.stat().st_mtime
    )


def get_champion_files():
    version_path = get_latest_version_path()

    return sorted(
        (version_path / "champions").glob("*.json")
    )


@pytest.mark.integration
@pytest.mark.parametrize(
    "champion_file",
    get_champion_files(),
    ids=lambda path: path.stem,
)

def test_champion_normalizes(champion_file):
    with champion_file.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)

    champion_id = champion_file.stem
    champion = raw_data["data"][champion_id]

    normalized = normalize_champion(
        champion,
        champion_file.parents[1].name,
    )

    assert normalized["patch_version"] == champion_file.parents[1].name

    assert set(normalized.keys()) == {
        "patch_version",
        "id",
        "name",
        "tags",
        "resource_type",
        "riot_metadata",
        "base_stats",
        "passive",
        "abilities",
    }
    assert set(normalized["riot_metadata"].keys()) == {
        "attack",
        "defense",
        "magic",
        "difficulty",
    }

    assert set(normalized["base_stats"].keys()) == {
        "hp",
        "hp_per_level",
        "resource",
        "resource_per_level",
        "hp_regen",
        "hp_regen_per_level",
        "resource_regen",
        "resource_regen_per_level",
        "armor",
        "armor_per_level",
        "magic_resist",
        "magic_resist_per_level",
        "attack_damage",
        "attack_damage_per_level",
        "attack_speed",
        "attack_speed_per_level",
        "attack_range",
        "move_speed",
        "crit",
        "crit_per_level",
    }

    assert set(normalized["passive"].keys()) == {
        "name",
        "description",
    }

    for ability in normalized["abilities"]:
        assert set(ability.keys()) == {
            "slot",
            "spell_id",
            "name",
            "description",
            "tooltip",
            "max_rank",
            "cooldowns",
            "costs",
            "cost_type",
            "ranges",
        }

    assert normalized["id"]
    assert normalized["name"]
    assert normalized["base_stats"]["hp"] > 0
    assert normalized["passive"]["name"]
    assert len(normalized["abilities"]) > 0
