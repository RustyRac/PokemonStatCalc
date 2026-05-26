import pytest
from src.calc import calculate_hp, calculate_stat, calculate_pokemon_stats


class TestHP:
    def test_hp_basic(self):
        result = calculate_hp(100, 31, 252, 50)

        assert isinstance(result, int)
        assert result > 0
        assert result != 0

    def test_hp_min_values(self):

        result = calculate_hp(1, 0, 0, 1)

        assert result > 10
        assert isinstance(result, int)

    @pytest.mark.parametrize(
        "base,iv,ev,level",
        [
            (50, 31, 0, 1),
            (50, 31, 252, 50),
            (100, 0, 0, 100),
            (150, 31, 252, 100),
            (1, 0, 0, 1),
        ],
    )
    def test_hp_param(self, base, iv, ev, level):
        result = calculate_hp(base, iv, ev, level)

        assert result > 0
        assert isinstance(result, int)


class TestStats:
    def test_stat_basic(self):

        result = calculate_stat(100, 31, 252, 50, 1.0)

        assert isinstance(result, int)
        assert result > 0

    def test_nature_increases_stat(self):

        boosted = calculate_stat(100, 31, 252, 50, 1.1)
        neutral = calculate_stat(100, 31, 252, 50, 1.0)

        assert boosted != neutral
        assert boosted > neutral

    def test_nature_decreases_stat(self):

        lowered = calculate_stat(100, 31, 252, 50, 0.9)
        neutral = calculate_stat(100, 31, 252, 50, 1.0)

        assert lowered < neutral
        assert lowered != neutral


class TestNegative:

    @pytest.mark.parametrize(
        "base,iv,ev,level,nature",
        [
            (50, 31, 0, 10, 1.2),
            (50, 31, 252, 100, 0.3),
            (100, 31, 252, 50, "adamant"),
        ],
    )
    def test_invalid_nature_type(self, base, iv, ev, level, nature):

        with pytest.raises(TypeError):
            calculate_stat(base, iv, ev, level, nature)

    @pytest.mark.parametrize(
        "base,iv,ev,level,nature",
        [
            (50, 32, 0, 10, 1.1),
            (50, 31, 256, 100, 0.9),
            (100, 31, 252, 101, 1.0),
        ],
    )
    def test_too_high_values(self, base, iv, ev, level, nature):

        with pytest.raises(ValueError):
            calculate_stat(base, iv, ev, level, nature)

    @pytest.mark.parametrize(
        "base,iv,ev,level,nature",
        [
            (50, -1, 0, 10, 1.1),
            (50, 31, -2, 100, 0.9),
            (100, 31, 252, -4, 1.0),
        ],
    )
    def test_negative_values(self, base, iv, ev, level, nature):
        with pytest.raises(ValueError):
            calculate_stat(base, iv, ev, level, nature)


class TestPokemonStats:
    def test_output_is_dict(self):

        base_stats = {
            "hp": 100,
            "attack": 100,
            "defense": 100,
            "sp_attack": 100,
            "sp_defense": 100,
            "speed": 100,
        }

        ivs = {k: 31 for k in base_stats}
        evs = {k: 252 for k in base_stats}

        result = calculate_pokemon_stats(
            base_stats,
            ivs,
            evs,
            50,
            {
                "hp": 1.0,
                "attack": 1.1,
                "defense": 1.0,
                "sp_attack": 1.0,
                "sp_defense": 1.0,
                "speed": 1.0,
            },
        )

        assert isinstance(result, dict)
        assert "hp" in result
        assert result["hp"] > 0
