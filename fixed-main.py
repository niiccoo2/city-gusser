import json
import random
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_cities_from_json():
    json_file_path = r"C:\Users\benel\OneDrive\Desktop\VS Code Projects\city-gusser\photos-database.json"
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            local_list_city = data.get("cities", [])
            #print(local_list_city)
        return local_list_city
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON file.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def grab_random_city(list_of_city):
    full_list = list_of_city
    city_hidden  = random.choice(full_list)
    print("Hidden City:", city_hidden)
    return city_hidden

def main():
    clear_console()
    cities = fetch_cities_from_json()
    if not cities:
        print("No cities found.")
        return
    city_hidden = grab_random_city(cities)
    guess_history = []
    attempt_number = 0
    clear_console()
    while True:
        current_guess = input("Guess a City.\n")
        current_guess = current_guess.lower().strip()

        if not current_guess:
            print("Please Enter A guess.")
            continue

        # Check if guess is correct
        if city_hidden["city"].lower().strip() == current_guess:
            print("YOU WIN!!!")
            attempt_number += 1
            break
        # Check if guess is a valid city in the list
        elif any(current_guess == c["city"].lower().strip() for c in cities):
            guess_history.append(current_guess)
            attempt_number += 1
            print("Guess Wrong But Valid.")
            print("Giving Hint.")
            print(f"Hint image: {city_hidden.get('image', 'No image available')}")
        else:
            print("Failed to understand guess.")

main()

