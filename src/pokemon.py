from dataclasses import dataclass
import json
import os


@dataclass
class Pokemon:

    name: str
    types: list[str]
    base_stats: dict

    level: int
    ivs: dict
    evs: dict
    nature: str

    battle_stats: dict

    def __str__(self):
        return f"{self.name.upper()}, Level: {self.level}, Type : {', '.join(self.types)}\nNature: {self.nature}\n\n Stats : {self.battle_stats}"

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "nature": self.nature,
            "ivs": self.ivs,
            "evs": self.evs,
        }

    def save(self, save_name, filename="./data/saved_pokemon.json"):

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                else:
                    data = {}
        else:
            data = {}
        data[save_name] = self.to_dict()

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
