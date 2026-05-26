import json

from src.pokemon import Pokemon


class TestPokemonInit:

    def test_create_pokemon(self):

        pokemon = Pokemon(
            name="pikachu",
            types=["electric"],
            base_stats={"hp": 35},
            level=50,
            ivs={"hp": 31},
            evs={"hp": 252},
            nature="timid",
            battle_stats={"hp": 142},
        )

        assert pokemon.name == "pikachu"
        assert pokemon.level == 50
        assert pokemon.nature == "timid"


class TestPokemonStr:
    def test_str_returns_string(self):

        pokemon = Pokemon(
            name="pikachu",
            types=["electric"],
            base_stats={},
            level=50,
            ivs={},
            evs={},
            nature="timid",
            battle_stats={},
        )

        result = str(pokemon)

        assert isinstance(result, str)

    def test_str_contains_name(self):

        pokemon = Pokemon(
            name="pikachu",
            types=["electric"],
            base_stats={},
            level=50,
            ivs={},
            evs={},
            nature="timid",
            battle_stats={},
        )

        result = str(pokemon)

        assert "PIKACHU" in result

    def test_str_contains_nature(self):

        pokemon = Pokemon(
            name="pikachu",
            types=["electric"],
            base_stats={},
            level=50,
            ivs={},
            evs={},
            nature="timid",
            battle_stats={},
        )

        result = str(pokemon)

        assert "timid" in result


class TestPokemonToDict:
    def test_to_dict_returns_dict(self):

        pokemon = Pokemon(
            name="pikachu",
            types=["electric"],
            base_stats={},
            level=50,
            ivs={"hp": 31},
            evs={"hp": 252},
            nature="timid",
            battle_stats={},
        )

        result = pokemon.to_dict()

        assert isinstance(result, dict)

    def test_to_dict_contains_keys(self):

        pokemon = Pokemon(
            name="pikachu",
            types=["electric"],
            base_stats={},
            level=50,
            ivs={"hp": 31},
            evs={"hp": 252},
            nature="timid",
            battle_stats={},
        )

        result = pokemon.to_dict()

        assert "name" in result
        assert "ivs" in result
        assert "evs" in result


class TestPokemonSave:

    def test_save_to_empty_file(self, tmp_path):

        file = tmp_path / "save.json"

        file.touch()

        pokemon = Pokemon(
            name="pikachu",
            types=["electric"],
            base_stats={},
            level=50,
            ivs={},
            evs={},
            nature="timid",
            battle_stats={},
        )

        pokemon.save("save1", file)

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "save1" in data

    def test_save_creates_file(self, tmp_path):

        file = tmp_path / "pokemon.json"

        pokemon = Pokemon(
            name="pikachu",
            types=["electric"],
            base_stats={},
            level=50,
            ivs={},
            evs={},
            nature="timid",
            battle_stats={},
        )
        pokemon.save("test_save", file)
        assert file.exists()

    def test_save_contains_pokemon(self, tmp_path):

        file = tmp_path / "pokemon.json"
        pokemon = Pokemon(
            name="pikachu",
            types=["electric"],
            base_stats={},
            level=50,
            ivs={},
            evs={},
            nature="timid",
            battle_stats={},
        )

        pokemon.save("test_save", file)

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "test_save" in data
        assert data["test_save"]["name"] == "pikachu"
