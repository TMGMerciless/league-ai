"""
League AI - Champion data normalization

Transforms raw Riot Data Dragon champion data into the internal
League AI champion schema.

Raw source data is never modified by this module.
"""

import json
from pathlib import Path


RAW_DATA_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/normalized")


def get_latest_local_version():
    versions = [
        path for path in RAW_DATA_DIR.iterdir()
        if path.is_dir()
    ]

    if not versions:
        raise FileNotFoundError(
            "No Data Dragon versions found in data/raw/"
        )

    return max(versions, key=lambda path: path.stat().st_mtime)


def normalize_champion(champion, patch_version):
    normalized_abilities = []

    ability_slots = ["Q", "W", "E", "R"]

    for slot, spell in zip(ability_slots, champion["spells"]):
        normalized_abilities.append({
            "slot":slot,
            "spell_id": spell["id"],
            "name": spell["name"],
            "description": spell["description"],
            "tooltip": spell["tooltip"],
            "max_rank": spell["maxrank"],
            "cooldowns": spell["cooldown"],
            "costs": spell["cost"],
            "cost_type": spell["costType"],
            "ranges": spell["range"],
        })

    normalized_champion = {
        "patch_version": patch_version,
        "id": champion["id"],
        "name": champion["name"],
        "tags": champion["tags"],
        "resource_type": champion["partype"],
        "riot_metadata": {
            "attack": champion["info"]["attack"],
            "defense": champion["info"]["defense"],
            "magic": champion["info"]["magic"],
            "difficulty": champion["info"]["difficulty"],
        },
        "base_stats": {
	    "hp": champion["stats"]["hp"],
	    "hp_per_level": champion["stats"]["hpperlevel"],

	    "resource": champion["stats"]["mp"],
	    "resource_per_level": champion["stats"]["mpperlevel"],

	    "hp_regen": champion["stats"]["hpregen"],
	    "hp_regen_per_level": champion["stats"]["hpregenperlevel"],

	    "resource_regen": champion["stats"]["mpregen"],
	    "resource_regen_per_level": champion["stats"]["mpregenperlevel"],

	    "armor": champion["stats"]["armor"],
	    "armor_per_level": champion["stats"]["armorperlevel"],

	    "magic_resist": champion["stats"]["spellblock"],
	    "magic_resist_per_level": champion["stats"]["spellblockperlevel"],

	    "attack_damage": champion["stats"]["attackdamage"],
	    "attack_damage_per_level": champion["stats"]["attackdamageperlevel"],

	    "attack_speed": champion["stats"]["attackspeed"],
	    "attack_speed_per_level": champion["stats"]["attackspeedperlevel"],

	    "attack_range": champion["stats"]["attackrange"],
	    "move_speed": champion["stats"]["movespeed"],

	    "crit": champion["stats"]["crit"],
	    "crit_per_level": champion["stats"]["critperlevel"],
        },
        "passive": {
            "name": champion["passive"]["name"],
            "description": champion["passive"]["description"],
        },
        "abilities": normalized_abilities,
    }

    return normalized_champion

def main():
    version_path = get_latest_local_version()

    champions_dir = version_path / "champions"
    champion_files = sorted(champions_dir.glob("*.json"))

    for champion_file in champion_files:
        with champion_file.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)

        champion_id = champion_file.stem
        champion = raw_data["data"][champion_id]

        normalized_champion = normalize_champion(champion,
            version_path.name,
        )

        output_file = (
            OUTPUT_DIR
            / version_path.name
            / "champions"
            / champion_file.name
        )

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with output_file.open("w", encoding="utf-8") as file:
            json.dump(normalized_champion, file, indent=2)

    print("Normalized champions:", len(champion_files))

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(normalized_champion, file, indent=2)

if __name__ == "__main__":
    main()
