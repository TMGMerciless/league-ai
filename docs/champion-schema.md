# Normalized Champion Schema

## Goal

Convert Riot Data Dragon champion data into a stable League AI representation.

Raw Riot data remains preserved separately.

## Champion

- id
- name
- tags
- resource_type

## Riot Metadata

- attack
- defense
- magic
- difficulty

## Base Stats

Preserve Riot's structured champion stats.

Examples:

- hp
- hp_per_level
- armor
- armor_per_level
- magic_resist
- magic_resist_per_level
- attack_damage
- attack_damage_per_level
- attack_speed
- move_speed

## Passive

- name
- description

## Abilities

Each ability should have:

- slot
- spell_id
- name
- description
- tooltip
- max_rank
- cooldowns
- costs
- cost_type
- ranges

## Design Principles

- Preserve raw source data separately.
- Prefer structured numeric values over *Burn display fields.
- Keep semantic text when mechanics are not fully represented numerically.
- Exclude presentation-only fields such as sprite coordinates.
- Do not infer gameplay mechanics that Riot data does not explicitly provide yet.
- Keep the schema patch-version aware.
