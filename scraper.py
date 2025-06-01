import requests
import os

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

# Example

info = get_city_info("Tokyo")
print(info.get('city'))
