# from openai import OpenAI
import os
import json
import random
import requests


def get_summary(city):
    with open("api.txt", "r") as api:
        key = api.read()
        client = OpenAI(api_key=key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"Write a two sentance summary of {city}. It is for a city gussing game so you can't give away the city is. Maybe some fun facts. DO NOT INCLUDE ANY LOCATIONS EX: EUROPE, SOUTH ASIA"},
            ],
            temperature=0,
        )

        return response.choices[0].message.content
    
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

### JSON file stuff ###

def pick_random_city(number_of_cities = 1, filepath = "./photos-database.json"):
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
    

def compare_city(city1, city2, filepath = "./photos-database.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
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
                output += " close"
            else:
                print("Grey (debug: far)")
                output += " far"
            return output
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON file.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []  




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
    print(geo_response)  # Add this line to see the full response
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
            print(f"Added {city_info['city']} to {json_file}")
        else:
            print(f"{city_info['city']} already in database.")
    else:
        print(f"City not found or error: {city_info.get('error') if city_info else 'Unknown error'}")


def city_api(city):
    info = get_city_info(city)
    add_city_to_json(city)

    if info and isinstance(info, dict):
        if 'error' in info:
            print(info['error'])
            return info['error']
        else:
            print(info.get('city'))
            return(info.get('city'))
    else:
        print('No data returned.')
        return ''


def logic():

    guess = input("Guess a city!\n")
    city = pick_random_city()
    print(compare_city(city["city"], guess))
    
# def get_city_data(city, data_type):
#     json_file_path = "./photos-database.json"
#     try:
#         with open(json_file_path, "r", encoding="utf-8") as file:
#             data = json.load(file)
#             local_list_city = data.get("cities", [])

#             if data_type == "all":
#                 return [city_data for city_data in local_list_city if city_data["city"].lower() == city.lower()]
#             else:
#                 for city_data in local_list_city:
#                     if city_data["city"].lower() == city.lower():
#                         print(city_data.get(data_type))
#                         return city_data.get(data_type)
#                 print(f"{city} not found or {data_type} not available.")
#                 return None
#     except FileNotFoundError:
#         print(f"Error: File not found at {json_file_path}")
#         return []
#     except json.JSONDecodeError:
#         print("Error: Failed to decode JSON file.")
#         return []
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []

