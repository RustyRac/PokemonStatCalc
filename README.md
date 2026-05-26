# Pokemon Stat Calculator

A Python terminal app, for calculating Pokemon stats based on their species, level, iv's, and iv's

## Pokemon stat calculation

In pokemon each pokemon has their own base stats, that are predetermined based on what Pokemon it is.
Additionally each pokemon has Individual values (iv's), that are determined when the pokemon is caught,they range from 0 to 31 in each stat. 
Pokemon also have Effort values (ev's), that go up when defeating other pokemon.
When you knock out the pokemon Gimmighoul pokemon who took part in combat are granted 1 ev in the stat special attack.
Ev's go up to 255, and the total amount of evs one pokemon can have is 510.
The level of the pokemon also impacts the stats.

$$
HP = \left( \left( \frac{2 \times Base + IV + \frac{EV}{4}}{100} \right) \times Level \right) + Level + 10
$$

$$
Stat = \left( \left( \frac{2 \times Base + IV + \frac{EV}{4}}{100} \right) \times Level + 5 \right) \times Nature
$$

The detailed explanation of how stats are calculated is located on bulbapedia.
https://bulbapedia.bulbagarden.net/wiki/Stat


## Instalation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the calculator

To run the calc, execute:
```
python main.py
```

### How to use

1. **Start**: The user is presented with 5 options to choose from, input a number and press enter to select.
2. **Possible choices**:
   1. Build pokemon: the user inputs the name, level, nature, ev's and iv's. The app calculates the stats of the pokemon, then the user can save the build by choosing (y/n) and inputing the save name
   2. The user can load a save of the pokemon build that was previously created by inputing the save name.
   3. Show the the list of save names that can be loaded.
   4. Delete a save by inputing the save name.
   5. Exit the app

## Structure
```
.
└── PokemonStatCalc/
   ├───data/
   │   ├── natures.json
   │   ├── pokemon_database.json
   │   └── saved_pokemon.json
   │
   ├───src/
   │   ├── app.py
   │   ├── calc.py
   │   ├── loader.py
   │   ├── pokemon.py
   │   ├── validators.py
   │   └── __init__.py
   │
   ├───tests/
   │   ├── test_app.py
   │   ├── test_calc.py
   │   ├── test_loader.py
   │   ├── test_pokemon.py
   │   ├── test_validators.py
   │   └── __init__.py
   ├── main.py
   ├──requirements.txt
   └── README.md
```
