import json
import pytest

from src.loader import (
    load_database,
    get_pokemon,
    get_nature,
    get_save,
    build_nature_modifiers,
    build_pokemon,
    load_pokemon,
    list_saves,
    delete_save,
)
from src.pokemon import Pokemon


class TestLoadDatabase:
    def test_load_valid_database(self, tmp_path):

        file = tmp_path / "test.json"
        sample_data = {"pikachu": {"type": "electric"}}

        with open(file, "w", encoding="utf-8") as f:
            json.dump(sample_data, f)

        result = load_database(file)

        assert isinstance(result, dict)
        assert "pikachu" in result

    def test_missing_file(self):
        with pytest.raises(FileNotFoundError):
            load_database("missing.json")

    def test_invalid_json(self, tmp_path):

        file = tmp_path / "bad.json"
        with open(file, "w", encoding="utf-8") as f:
            f.write("{bad json}")

        with pytest.raises(json.JSONDecodeError):
            load_database(file)


class TestGetPokemon:
    @pytest.mark.parametrize(
        "name",
        [
            "goomy",
            "guzzlord",
            "gulpin",
        ],
    )
    def test_existing_pokemon(self, name):
        result = get_pokemon(name)

        assert isinstance(result, dict)

    def test_case_insensitive(self):

        lower = get_pokemon("pikachu")
        upper = get_pokemon("PIKACHU")

        assert lower == upper

    def test_invalid_pokemon(self):

        with pytest.raises(KeyError):
            get_pokemon("Augumon")


class TestGetNature:
    @pytest.mark.parametrize("nature", ["adamant", "modest", "timid"])
    def test_valid_nature(self, nature):

        result = get_nature(nature)
        assert isinstance(result, dict)

    def test_invalid_nature(self):

        with pytest.raises(KeyError):
            get_nature("happy")


class TestBuildNatureModifiers:
    def test_adamant_modifiers(self):

        nature = {"increase": "attack", "decrease": "special-attack"}

        result = build_nature_modifiers(nature)

        assert result["attack"] == 1.1
        assert result["special-attack"] == 0.9

    def test_neutral_nature(self):

        nature = {"increase": None, "decrease": None}

        result = build_nature_modifiers(nature)
        assert all(value == 1.0 for value in result.values())


class TestBuildPokemon:

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

    def test_returns_pokemon(self):

        pokemon = build_pokemon("pikachu", self.ivs, self.evs, 50, "adamant")

        assert isinstance(pokemon, Pokemon)

    def test_correct_name(self):

        pokemon = build_pokemon("pikachu", self.ivs, self.evs, 50, "adamant")

        assert pokemon.name == "pikachu"

    def test_has_battle_stats(self):

        pokemon = build_pokemon("pikachu", self.ivs, self.evs, 50, "adamant")

        assert isinstance(pokemon.battle_stats, dict)

    def test_invalid_pokemon(self):

        with pytest.raises(Exception):

            build_pokemon("fakepokemon", self.ivs, self.evs, 50, "adamant")

    def test_invalid_nature(self):

        with pytest.raises(Exception):

            build_pokemon("pikachu", self.ivs, self.evs, 50, "supernature")


class TestGetSave:
    def test_existing_save(self):

        saves = {"testsave": {"name": "pikachu"}}

        result = get_save("testsave", saves)

        assert result["name"] == "pikachu"

    def test_missing_save(self):
        saves = {}

        with pytest.raises(KeyError):
            get_save("missing", saves)



class TestLoadPokemon:

    def create_save_file(self, file):

        save_data = {
            "testsave": {
                "name": "pikachu",
                "level": 50,
                "nature": "adamant",
                "ivs": {
                    "hp": 31,
                    "attack": 31,
                    "defense": 31,
                    "special-attack": 31,
                    "special-defense": 31,
                    "speed": 31,
                },
                "evs": {
                    "hp": 0,
                    "attack": 252,
                    "defense": 0,
                    "special-attack": 0,
                    "special-defense": 4,
                    "speed": 252,
                },
            }
        }

        with open(file, "w", encoding="utf-8") as f:
            json.dump(save_data, f)

    def test_load_returns_pokemon(self, tmp_path):

        file = tmp_path / "save.json"

        self.create_save_file(file)

        pokemon = load_pokemon("testsave", file)

        assert isinstance(pokemon, Pokemon)

    def test_loaded_pokemon_name(self, tmp_path):

        file = tmp_path / "save.json"

        self.create_save_file(file)

        pokemon = load_pokemon("testsave", file)

        assert pokemon.name == "pikachu"

    def test_loaded_pokemon_level(self, tmp_path):

        file = tmp_path / "save.json"

        self.create_save_file(file)

        pokemon = load_pokemon("testsave", file)

        assert pokemon.level == 50

    def test_missing_save_file(self):

        with pytest.raises(FileNotFoundError):

            load_pokemon("test", "missing.json")

    def test_missing_save_name(self, tmp_path):

        file = tmp_path / "save.json"

        self.create_save_file(file)

        with pytest.raises(KeyError):

            load_pokemon("wrongsave", file)

    class TestListSaves:

        def test_missing_save_file(self):
            with pytest.raises(ValueError):
                list_saves("missing.json")

        def test_lists_saves(self, tmp_path, capsys):
            file = tmp_path / "save.json"

            data = {"save1": {}, "save2": {}}

            with open(file, "w", encoding="utf-8") as f:
                json.dump(data, f)

            list_saves(file)

            captured = capsys.readouterr()

            assert "save1" in captured.out
            assert "save2" in captured.out

        def test_empty_save_file(self, tmp_path, capsys):
            file = tmp_path / "save.json"

            with open(file, "w", encoding="utf-8") as f:
                json.dump({}, f)

            list_saves(file)

            captured = capsys.readouterr()

            assert captured.out == ""


class TestDeleteSave:

    def create_save_file(self, file):

        data = {"save1": {"name": "pikachu"}, "save2": {"name": "charizard"}}

        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def test_delete_existing_save(self, tmp_path):

        file = tmp_path / "save.json"

        self.create_save_file(file)

        delete_save("save1", file)

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "save1" not in data
        assert "save2" in data

    def test_missing_save_file(self):

        with pytest.raises(ValueError):

            delete_save("save1", "missing.json")

    def test_missing_save_name(self, tmp_path):

        file = tmp_path / "save.json"

        self.create_save_file(file)

        with pytest.raises(ValueError):

            delete_save("wrongsave", file)

    def test_delete_last_save(self, tmp_path):

        file = tmp_path / "save.json"

        data = {"save1": {"name": "pikachu"}}

        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f)

        delete_save("save1", file)

        with open(file, "r", encoding="utf-8") as f:
            result = json.load(f)

        assert result == {}
