import json
import random
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def pick_random_city(number_open):
    json_file_path = r"./photos-database.json"
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            local_list_city = data.get("cities", [])
            
            random_selections = []

            for i in range(number_open):
                selected = random.choice(local_list_city)
                random_selections.append(selected)
                print(selected)

        return random_selections
    
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON file.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_city_data(city, data_type):
    json_file_path = r"./photos-database.json"
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            local_list_city = data.get("cities", [])

            if data_type == "all":
                return [city_data for city_data in local_list_city if city_data["city"].lower() == city.lower()]
            else:
                for city_data in local_list_city:
                    if city_data["city"].lower() == city.lower():
                        print(city_data.get(data_type))
                        return city_data.get(data_type)
                print(f"{city} not found or {data_type} not available.")
                return None
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON file.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

get_city_data("Boston", "country")