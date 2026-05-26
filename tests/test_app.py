from src.app import input_stats, create_pokemon_menu, load_pokemon_menu, run


class TestInputStats:
    def test_input_stats(self, monkeypatch):

        inputs = iter(["31", "31", "31", "31", "31", "31"])

        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = input_stats("IV")

        assert result["hp"] == 31
        assert result["speed"] == 31


class TestCreatePokemonMenu:
    def test_create_pokemon(self, monkeypatch):

        inputs = iter(
            [
                "pikachu",
                "50",
                "adamant",
                "31",
                "31",
                "31",
                "31",
                "31",
                "31",
                "0",
                "252",
                "0",
                "0",
                "4",
                "252",
                "n",
            ]
        )

        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        called = False

        def fake_build():
            nonlocal called
            called = True

            class FakePokemon:
                def __str__(self):
                    return "pokemon"

            return FakePokemon()

        monkeypatch.setattr("src.app.build_pokemon", fake_build)

        create_pokemon_menu()

        assert called is True


class TestLoadPokemonMenu:
    def test_load_pokemon(self, monkeypatch):

        monkeypatch.setattr("builtins.input", lambda _: "testsave")

        called = False

        def fake_load():
            nonlocal called
            called = True

            class FakePokemon:
                def __str__(self):
                    return "pokemon"

            return FakePokemon()

        monkeypatch.setattr("src.app.load_pokemon", fake_load)

        load_pokemon_menu()

        assert called is True


class TestRun:
    def test_exit(self, monkeypatch, capsys):

        inputs = iter(["5"])

        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        run()

        captured = capsys.readouterr()

        assert "Goodbye" in captured.out

    def test_invalid_choice(self, monkeypatch, capsys):

        inputs = iter(["999", "5"])

        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        run()

        captured = capsys.readouterr()

        assert "Invalid choice" in captured.out

    def test_menu_option_1(self, monkeypatch):

        inputs = iter(["1", "5"])

        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        called = False

        def fake_create():
            nonlocal called
            called = True

        monkeypatch.setattr("src.app.create_pokemon_menu", fake_create)

        run()

        assert called is True

    def test_menu_option_2(self, monkeypatch):

        inputs = iter(["2", "5"])

        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        called = False

        def fake_load():
            nonlocal called
            called = True

        monkeypatch.setattr("src.app.load_pokemon_menu", fake_load)

        run()

        assert called is True

    def test_menu_option_3(self, monkeypatch):

        inputs = iter(["3", "5"])

        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        called = False

        def fake_list():
            nonlocal called
            called = True

        monkeypatch.setattr("src.app.list_saves", fake_list)

        run()

        assert called is True

    def test_value_error_handling(self, monkeypatch, capsys):

        inputs = iter(["1", "5"])

        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        def fake_create():
            raise ValueError("Test error")

        monkeypatch.setattr("src.app.create_pokemon_menu", fake_create)

        run()

        captured = capsys.readouterr()

        assert "ERROR" in captured.out

    def test_key_error_handling(self, monkeypatch, capsys):

        inputs = iter(["2", "5"])

        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        def fake_load():
            raise KeyError

        monkeypatch.setattr("src.app.load_pokemon_menu", fake_load)

        run()

        captured = capsys.readouterr()

        assert "Save not found" in captured.out
