def validate_ivs(ivs):

    for value in ivs.values():
        if not isinstance(value, int):
            print(value)
            raise TypeError("IV must be an integer")
        if value < 0 or value > 31:
            raise ValueError("IV must be between 0 and 31")


def validate_evs(evs):

    for value in evs.values():
        if not isinstance(value, int):
            raise TypeError("EV must be an integer")
        if value < 0 or value > 255:
            raise ValueError("EV must be between 0 and 255")

    total = sum(evs.values())

    if total > 510:
        raise ValueError(f"Total EVs cannot exceed 510 (got {total})")


def validate_level(level):
    if not isinstance(level, int):
        raise TypeError("Level must be an integer")
    if level < 1 or level > 100:
        raise ValueError("Level must be between 1 and 100")


def validate_stat_calc(iv, ev, level, nature_modifier):
    if 0 > iv or iv > 31:
        raise ValueError("IV must be between 0 and 31")
    if 0 > ev or ev > 252:
        raise ValueError("EV must be between 0 and 252")
    if nature_modifier not in [1.1, 1.0, 0.9]:
        raise TypeError("nature modifier is not valid")
    validate_level(level)


def validate_hp_calc(iv, ev, level):
    if 0 > iv or iv > 31:
        raise ValueError("IV must be between 0 and 31")
    if 0 > ev or ev > 252:
        raise ValueError("EV must be between 0 and 252")
    validate_level(level)


def validate_nature(nature, nature_db):
    if not isinstance(nature, str):
        raise TypeError("nature must be a string")
    if nature.lower() not in nature_db:
        raise ValueError(f"Nature '{nature}' does not exist")


def validate_species(name, pokemon_db):
    if not isinstance(name, str):
        raise TypeError("Name must be a string")
    if name.lower() not in pokemon_db:
        raise ValueError(f"{name} does not exist")


def validate_pokemon_build(name, ivs, evs, level, nature, pokemon_db, nature_db):

    validate_species(name, pokemon_db)
    validate_ivs(ivs)
    validate_evs(evs)
    validate_level(level)
    validate_nature(nature, nature_db)
