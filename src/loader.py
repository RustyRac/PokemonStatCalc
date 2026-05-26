import json
from src.pokemon import Pokemon
from src.calc import calculate_pokemon_stats
from src.validators import validate_pokemon_build
import os


def load_database(db):
    with open(db, "r", encoding="utf-8") as f:
        return json.load(f)


POKEMON_DB = load_database("./data/pokemon_database.json")
NATURE_DB = load_database("./data/natures.json")


def get_pokemon(name: str):
    return POKEMON_DB[name.lower()]


def get_nature(name: str):
    return NATURE_DB[name]


def get_save(name: str, save_data):
    return save_data[name]


def build_nature_modifiers(nature_data):

    modifiers = {
        "hp": 1.0,
        "attack": 1.0,
        "defense": 1.0,
        "special-attack": 1.0,
        "special-defense": 1.0,
        "speed": 1.0,
    }

    increase = nature_data["increase"]
    decrease = nature_data["decrease"]

    if increase:
        modifiers[increase] = 1.1

    if decrease:
        modifiers[decrease] = 0.9

    return modifiers


def build_pokemon(name: str, ivs, evs, level, nature):
    validate_pokemon_build(name, ivs, evs, level, nature, POKEMON_DB, NATURE_DB)
    pokedata = get_pokemon(name)
    natdata = get_nature(nature)
    nature_modifiers = build_nature_modifiers(natdata)
    return Pokemon(
        name=pokedata["name"],
        base_stats=pokedata["base_stats"],
        types=pokedata["types"],
        level=level,
        ivs=ivs,
        evs=evs,
        nature=nature,
        battle_stats=calculate_pokemon_stats(
            pokedata["base_stats"], ivs, evs, level, nature_modifiers
        ),
    )


def load_pokemon(save_name, filename="./data/saved_pokemon.json"):

    with open(filename, "r", encoding="utf-8") as f:
        save_data = json.load(f)

    pokedata = get_save(save_name, save_data)
    basedata = get_pokemon(pokedata["name"])
    natdata = get_nature(pokedata["nature"])
    nature_modifiers = build_nature_modifiers(natdata)
    validate_pokemon_build(
        basedata["name"],
        pokedata["ivs"],
        pokedata["evs"],
        pokedata["level"],
        pokedata["nature"],
        POKEMON_DB,
        NATURE_DB,
    )
    return Pokemon(
        name=basedata["name"],
        base_stats=basedata["base_stats"],
        types=basedata["types"],
        level=pokedata["level"],
        ivs=pokedata["ivs"],
        evs=pokedata["evs"],
        nature=pokedata["nature"],
        battle_stats=calculate_pokemon_stats(
            basedata["base_stats"],
            pokedata["ivs"],
            pokedata["evs"],
            pokedata["level"],
            nature_modifiers,
        ),
    )


def list_saves(filename="./data/saved_pokemon.json"):

    if not os.path.exists(filename):
        raise ValueError("Save file does not exist")

    count = 1
    with open(filename, "r", encoding="utf-8") as f:
        save_data = json.load(f)
    for save_name in save_data.keys():
        print(f"{count}. {save_name}")
        count += 1


def delete_save(save_name, filename="./data/saved_pokemon.json"):

    if not os.path.exists(filename):
        raise ValueError("Save file does not exist")

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read().strip()
        data = json.loads(content) if content else {}

    if save_name not in data:
        raise ValueError(f"Save '{save_name}' does not exist")

    del data[save_name]

    with open(filename, "w", encoding="utf-8") as f:

        json.dump(data, f, indent=2)
