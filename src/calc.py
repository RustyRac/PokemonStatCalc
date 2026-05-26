import math
from src.validators import validate_hp_calc, validate_stat_calc


def calculate_hp(base, iv, ev, level):
    validate_hp_calc(iv, ev, level)
    hp = math.floor(((2 * base + iv + math.floor(ev / 4)) * level) / 100) + level + 10
    return hp


def calculate_stat(base, iv, ev, level, nature=1.0):
    validate_stat_calc(iv, ev, level, nature)
    stat = math.floor(((2 * base + iv + math.floor(ev / 4)) * level) / 100) + 5
    return math.floor(stat * nature)


def calculate_pokemon_stats(base_stats, ivs, evs, level, nature_modifiers):
    final_stats = {}

    for stat in base_stats:

        if stat == "hp":
            final_stats[stat] = calculate_hp(
                base_stats[stat], ivs[stat], evs[stat], level
            )
        else:
            final_stats[stat] = calculate_stat(
                base_stats[stat], ivs[stat], evs[stat], level, nature_modifiers[stat]
            )

    return final_stats
