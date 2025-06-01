import requests
import os
import json

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

    if info and isinstance(info, dict):
        if 'error' in info:
            print(info['error'])
        else:
            print(info.get('city'))
    else:
        print('No data returned.')

    add_city_to_json(city)
