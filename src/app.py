from src.loader import load_pokemon
from src.loader import build_pokemon
from src.loader import delete_save
from src.loader import list_saves


def input_stats(stat_name):
    stat_dict = {}
    stat_names = [
        "hp",
        "attack",
        "defense",
        "special-attack",
        "special-defense",
        "speed",
    ]
    for stat in stat_names:
        value = int(input(f"{stat_name} {stat}: "))
        stat_dict[stat] = value

    return stat_dict


def create_pokemon_menu():

    species = input("Pokemon: ").lower()
    level = int(input("Level: "))
    nature = input("Nature: ").lower()

    print("\nEnter IVs")
    ivs = input_stats("IV")

    print("\nEnter EVs")
    evs = input_stats("EV")

    pokemon = build_pokemon(species, ivs, evs, level, nature)

    print("\n=== POKEMON ===")
    print(pokemon)

    save = input("\nSave this Pokemon? (y/n): ").lower()

    if save == "y":

        save_name = input("Save name: ")

        pokemon.save(save_name)
        print("Pokemon saved.")


def load_pokemon_menu():

    save_name = input("Save name: ")

    pokemon = load_pokemon(save_name)

    print("\n=== LOADED POKEMON ===")
    print(pokemon)


def run():

    while True:

        print("\n=== POKEMON CALCULATOR ===")
        print("1. Build Pokemon")
        print("2. Load Pokemon")
        print("3. Show save names")
        print("4. Delete save")
        print("5. Exit")
        choice = input("Choice: ")

        try:

            if choice == "1":

                create_pokemon_menu()

            elif choice == "2":
                load_pokemon_menu()

            elif choice == "3":
                list_saves()

            elif choice == "4":
                save_name = input("Save name: ")
                delete_save(save_name)
                print(f"Pokemon save: {save_name} has been deleted.")

            elif choice == "5":
                print("Goodbye.")
                break

            else:
                print("Invalid choice.")

        except ValueError as e:
            print("\nERROR:")
            print(e)

        except KeyError:
            print("\nSave not found.")
