from openai import OpenAI #type: ignore
import os
import json
import random
import requests #type: ignore

def get_summary(city):
    with open("api.txt", "r") as api:
        key = api.read()
        client = OpenAI(api_key=key)

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "user", "content": f"Write a two sentance summary of {city}. It is for a city gussing game so you can't give away the city is. Maybe some fun facts. DO NOT INCLUDE ANY LOCATIONS EX: EUROPE, SOUTH ASIA"},
            ],
            temperature=0,
        )

        return response.choices[0].message.content
    
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

### JSON file stuff ###

def pick_random_city(number_of_cities = 1, filepath = "./photos-database-scraper.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

            local_list_city = data.get("cities", [])
                
            random_selections = []

            for i in range(number_of_cities):
                selected = random.choice(local_list_city)
                random_selections.append(selected)
                #print(selected)

        return random_selections
    
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON file.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
def compare_city(city1, city2, mode, filepath = "./photos-database-scraper.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            local_list_city = data.get("cities", [])

            city1_data = next((c for c in local_list_city if c["city"].lower() == city1.lower()), None)
            city2_data = next((c for c in local_list_city if c["city"].lower() == city2.lower()), None)

            if not city1_data or not city2_data:
                return "One or both cities not found."

            city_lat = city1_data.get('lat') if city1_data.get('lat') is not None else city1_data.get('latitude')
            city_lon = city1_data.get('lon') if city1_data.get('lon') is not None else city1_data.get('longitude')
            guess_lat = city2_data.get('lat') if city2_data.get('lat') is not None else city2_data.get('latitude')
            guess_lon = city2_data.get('lon') if city2_data.get('lon') is not None else city2_data.get('longitude')

            try:
                city_lat = float(city_lat)
                city_lon = float(city_lon)
                guess_lat = float(guess_lat)
                guess_lon = float(guess_lon)
            except (TypeError, ValueError):
                return "Missing location data."

            output = ""

            if mode == "dir":
                if abs(city_lon - guess_lon) > abs(city_lat - guess_lat):
                    if city_lon > guess_lon:
                        output = "West"  # Flipped from East
                    else:
                        output = "East"  # Flipped from West
                elif mode == "cardinal":
                    if city_lat > guess_lat:
                        output = "North"
                    else:
                        output = "South"
            else:
                if abs((guess_lon + guess_lat) - (city_lon + city_lat)) < 20:
                    output = "(Yellow)"
                else:
                    output = "(Grey)"

            return output
    except FileNotFoundError:
        return "File not found."
    except json.JSONDecodeError:
        return "JSON decode error."
    except Exception as e:
        return f"Error: {e}"
    
def compare_country(city1, city2, filepath = "./photos-database-scraper.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            local_list_city = data.get("cities", [])

            city1_data = next((c for c in local_list_city if c["country"].lower() == city1.lower()), None)
            city2_data = next((c for c in local_list_city if c["country"].lower() == city2.lower()), None)

            if not city1_data or not city2_data:
                return "One or both cities not found."

            city_lat = city1_data.get('lat') if city1_data.get('lat') is not None else city1_data.get('latitude')
            city_lon = city1_data.get('lon') if city1_data.get('lon') is not None else city1_data.get('longitude')
            guess_lat = city2_data.get('lat') if city2_data.get('lat') is not None else city2_data.get('latitude')
            guess_lon = city2_data.get('lon') if city2_data.get('lon') is not None else city2_data.get('longitude')

            try:
                city_lat = float(city_lat)
                city_lon = float(city_lon)
                guess_lat = float(guess_lat)
                guess_lon = float(guess_lon)
            except (TypeError, ValueError):
                return "Missing location data."

            output = ""
            if abs((guess_lon + guess_lat) - (city_lon + city_lat)) < 20:
                   output = "(Yellow)"
            else:
                output = "(Grey)"

            return output
    except FileNotFoundError:
        return "File not found."
    except json.JSONDecodeError:
        return "JSON decode error."
    except Exception as e:
        return f"Error: {e}"

def load_opencage_key():
    env_path = os.path.join(os.path.dirname(__file__), 'scraper.env')
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('API_KEY'):
                    return line.split('=', 1)[1].strip().strip('"')
    except Exception as e:
        print(f"Could not load API key: {e}")
        return None

OPENCAGE_API_KEY = load_opencage_key()

def get_city_info(city):
    city = city.strip()
    oc_url = "https://api.opencagedata.com/geocode/v1/json"
    oc_params = {
        "q": city,
        "key": OPENCAGE_API_KEY
    }
    geo_response = requests.get(oc_url, params=oc_params).json()
    #print(geo_response)  # Add this line to see the full response
    if not geo_response["results"]:
        return {"error": "City not found"}
    location = geo_response["results"][0]
    lat = location["geometry"]["lat"]
    lng = location["geometry"]["lng"]
    country = location["components"].get("country", "Unknown")
    return {
        "city": city,
        "country": country,
        "latitude": lat,
        "longitude": lng
    }

def add_city_to_json(city):
    city_info = get_city_info(city)
    if city_info and 'error' not in city_info:
        json_file = 'photos-database-scraper.json'
        # Read existing data
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = {"cities": []}
        # Add new city
        if "cities" not in data or not isinstance(data["cities"], list):
            data["cities"] = []
        # Avoid duplicates
        if not any(c.get('city', '').lower() == city_info['city'].lower() for c in data['cities']):
            data["cities"].append(city_info)
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            # print(f"Added {city_info['city']} to {json_file}")
        #else:
            #print(f"{city_info['city']} already in database.")
    else:
        # print(f"City not found or error: {city_info.get('error') if city_info else 'Unknown error'}")
        pass

def city_api(city):
    info = get_city_info(city)
    add_city_to_json(city)
    if info and isinstance(info, dict):
        if 'error' in info:
            print(info['error'])
            return None
        else:
            return info  # Return the full dict
    else:
        print('No data returned.')
        return None

def logic():
    # Pick the random city ONCE per game, not every guess
    city_info_list = pick_random_city(1, filepath="photos-database-scraper.json")
    if not city_info_list:
        print("No cities in database.")
        return "No Cities In DataBase"
    city_info = city_info_list[0]
    print(f"City: {city_info.get('city', 'Unknown City')}")
    while True:
        guess = input("Guess a city!\n")
        guess_normalized = guess.lower().replace('city', '').replace('.', '').replace(',', '').strip()
        guess_info = city_api(guess)
        if not guess_info:
            print("Invalid guess.")
            continue

        

        target_city_normalized = city_info.get('city', '').lower().replace('city', '').replace('.', '').replace(',', '').strip()
        guess_city_normalized = guess_info.get('city', '').lower().replace('city', '').replace('.', '').replace(',', '').strip()
        target_country_normalized = city_info.get('country', '').lower().strip()
        guess_country_normalized = guess_info.get('country', '').lower().strip()

        print(target_city_normalized)

        def get_state(city_dict):
            components = city_dict.get('components', {})
            return components.get('state', '').lower().strip() if components else ''

        guess_state = get_state(guess_info)
        target_state = get_state(city_info)

        if target_country_normalized == 'united states' and guess_country_normalized == 'united states' and guess_state and target_state:
            if guess_state == target_state:
                country_hint = f"{guess_state.title()} (green)"
            else:
                country_hint = f"{guess_state.title()} (grey)"
        elif guess_country_normalized == target_country_normalized:
            country_hint = f"{guess_info.get('country')} (green)"
        else:
            if guess_info.get('country') and city_info.get('country'):
                relative_distance_country = compare_country(guess_info.get('country'), city_info.get('country'))
                if relative_distance_country == "(Yellow)":
                    country_hint = f"{guess_info.get('country')} (yellow)"
                else:
                    country_hint = f"{guess_info.get('country')} (grey)"
            else:
                country_hint = "Unknown"

        if guess_city_normalized == target_city_normalized:
            print(f"Correct! You win! {country_hint}")
            return(f"Correct! You win! {country_hint}")

        direction = compare_city(guess, city_info.get('city'), "dir")
        relative_distance_city = compare_city(guess, city_info.get('city'), "cardinal")
        print(f"{country_hint}, {guess_info.get('city')} {relative_distance_city}, {direction}")

if __name__ == "__main__":
    logic()