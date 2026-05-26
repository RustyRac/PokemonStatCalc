import pytest

from src.validators import (
    validate_ivs,
    validate_evs,
    validate_level,
    validate_nature,
    validate_species,
    validate_pokemon_build,
)
from src.loader import NATURE_DB, POKEMON_DB


class TestIV:

    @pytest.mark.parametrize(
        "ivs",
        [
            {
                "hp": 0,
                "attack": 0,
                "defense": 0,
                "special-attack": 0,
                "special-defense": 0,
                "speed": 0,
            },
            {
                "hp": 15,
                "attack": 15,
                "defense": 15,
                "special-attack": 15,
                "special-defense": 15,
                "speed": 15,
            },
            {
                "hp": 31,
                "attack": 31,
                "defense": 31,
                "special-attack": 31,
                "special-defense": 31,
                "speed": 31,
            },
        ],
    )
    def test_valid_iv(self, ivs):
        assert validate_ivs(ivs) is None

    @pytest.mark.parametrize(
        "ivs",
        [
            {
                "hp": -1,
                "attack": 0,
                "defense": 0,
                "special-attack": 0,
                "special-defense": 0,
                "speed": 0,
            },
            {
                "hp": 15,
                "attack": 15,
                "defense": -4,
                "special-attack": 15,
                "special-defense": 15,
                "speed": 15,
            },
            {
                "hp": 31,
                "attack": 31,
                "defense": 31,
                "special-attack": 31,
                "special-defense": -999,
                "speed": 31,
            },
        ],
    )
    def test_negative_ivs(self, ivs):
        with pytest.raises(ValueError):
            validate_ivs(ivs)

    @pytest.mark.parametrize(
        "ivs",
        [
            {
                "hp": "Guh",
                "attack": 0,
                "defense": 0,
                "special-attack": 0,
                "special-defense": 0,
                "speed": 0,
            },
            {
                "hp": 15,
                "attack": 15,
                "defense": 1.5,
                "special-attack": 15,
                "special-defense": 15,
                "speed": 15,
            },
            {
                "hp": 31,
                "attack": 31,
                "defense": 31,
                "special-attack": 31,
                "special-defense": [],
                "speed": 31,
            },
        ],
    )
    def test_invalid_iv_type(self, ivs):
        with pytest.raises(TypeError):
            validate_ivs(ivs)


class TestEV:

    @pytest.mark.parametrize(
        "evs",
        [
            {
                "hp": 0,
                "attack": 0,
                "defense": 0,
                "special-attack": 0,
                "special-defense": 0,
                "speed": 0,
            },
            {
                "hp": 15,
                "attack": 0,
                "defense": 0,
                "special-attack": 125,
                "special-defense": 15,
                "speed": 15,
            },
            {
                "hp": 255,
                "attack": 0,
                "defense": 30,
                "special-attack": 0,
                "special-defense": 0,
                "speed": 0,
            },
        ],
    )
    def test_valid_ev(self, evs):
        assert validate_evs(evs) is None

    @pytest.mark.parametrize(
        "evs",
        [
            {
                "hp": -1,
                "attack": 0,
                "defense": 0,
                "special-attack": 0,
                "special-defense": 0,
                "speed": 0,
            },
            {
                "hp": 15,
                "attack": 15,
                "defense": -4,
                "special-attack": 15,
                "special-defense": 15,
                "speed": 15,
            },
            {
                "hp": 31,
                "attack": 31,
                "defense": 31,
                "special-attack": 31,
                "special-defense": -999,
                "speed": 31,
            },
        ],
    )
    def test_negative_evs(self, evs):
        with pytest.raises(ValueError):
            validate_ivs(evs)

    def test_ev_total_too_high(self):

        evs = {
            "hp": 252,
            "attack": 252,
            "defense": 252,
            "sp_attack": 0,
            "sp_defense": 0,
            "speed": 0,
        }

        with pytest.raises(ValueError):
            validate_evs(evs)

    @pytest.mark.parametrize(
        "evs",
        [
            {
                "hp": "Guh",
                "attack": 0,
                "defense": 0,
                "special-attack": 0,
                "special-defense": 0,
                "speed": 0,
            },
            {
                "hp": 15,
                "attack": 15,
                "defense": 1.5,
                "special-attack": 15,
                "special-defense": 15,
                "speed": 15,
            },
            {
                "hp": 31,
                "attack": 31,
                "defense": 31,
                "special-attack": 31,
                "special-defense": [],
                "speed": 31,
            },
        ],
    )
    def test_invalid_ev_type(self, evs):
        with pytest.raises(TypeError):
            validate_ivs(evs)


class TestLevel:

    @pytest.mark.parametrize("level", [1, 50, 100])
    def test_valid_level(self, level):
        assert validate_level(level) is None

    @pytest.mark.parametrize("level", [0, -1, 101, 999])
    def test_level_out_of_range(self, level):
        with pytest.raises(ValueError):
            validate_level(level)

    def test_invalid_level_type(self):
        level = "dwa"
        with pytest.raises(TypeError):
            validate_level(level)


class TestNature:

    def test_valid_nature(self):
        nature = "adamant"
        assert validate_nature(nature, NATURE_DB) is None

    def test_invalid_nature_name(self):
        nature = "adamantini"
        with pytest.raises(ValueError):
            validate_nature(nature, NATURE_DB)

    def test_invalid_nature_type(self):
        nature = 10
        with pytest.raises(TypeError):
            validate_nature(nature, NATURE_DB)


class TestSpecies:
    def test_valid_species(self):
        name = "goomy"
        assert validate_species(name, POKEMON_DB) is None

    def test_invalid_species_name(self):
        name = "Orkonoin"
        with pytest.raises(ValueError):
            validate_species(name, POKEMON_DB)

    def test_invalid_species_type(self):
        name = 59
        with pytest.raises(TypeError):
            validate_species(name, POKEMON_DB)


class TestPokemon:
    def test_valid_pokemon(self):
        name = "goomy"
        level = 50
        nature = "adamant"
        ivs = {
            "hp": 31,
            "attack": 31,
            "defense": 31,
            "special-attack": 31,
            "special-defense": 31,
            "speed": 31,
        }
        evs = {
            "hp": 0,
            "attack": 252,
            "defense": 0,
            "special-attack": 0,
            "special-defense": 4,
            "speed": 252,
        }
        assert (
            validate_pokemon_build(name, ivs, evs, level, nature, POKEMON_DB, NATURE_DB)
            is None
        )
