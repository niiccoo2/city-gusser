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
            
            if number_open == 1:
                selected = random.choice(local_list_city)
                random_selections = selected
                print(selected)
            else:
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

def compare_city(city1, city2):
    json_file_path = r"./photos-database.json"
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            local_list_city = data.get("cities", [])

            city1_data = next((c for c in local_list_city if c["city"].lower() == city1.lower()), None)
            city2_data = next((c for c in local_list_city if c["city"].lower() == city2.lower()), None)

            if not city1_data or not city2_data:
                print("One or both cities not found.")
                return None

            city_lat = city1_data.get('lat')
            city_lon = city1_data.get('lon')
            guess_lat = city2_data.get('lat')
            guess_lon = city2_data.get('lon')

            output = ""

            if abs(city_lon - guess_lon) > abs(city_lat - guess_lat):
                if city_lon > guess_lon:
                    print("East")
                    output = "East"
                else:
                    print("West")
                    output = "West"
            else:
                if city_lat > guess_lat:
                    print("North")
                    output = "North"
                else:
                    print("South")
                    output = "South"
            print(city_lat, city_lon)
            print(guess_lat, guess_lon)

            if abs((guess_lon + guess_lat) - (city_lon + city_lat)) < 20:
                print("Yellow (debug: close)")
                output += " Yellow (debug: close)"
            else:
                print("Grey (debug: far)")
                output += " Grey (debug: far)"
            return output
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON file.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []  