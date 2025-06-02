from openai import OpenAI #type: ignore
import os
import json
import random
import requests
import requests
from bs4 import BeautifulSoup #type: ignore
import json
import sys
sys.path.append('.')


def get_summary(city):
    with open("api.txt", "r") as api:
        key = api.read()
        client = OpenAI(api_key=key)

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "user", "content": f"Write a two sentance summary of {city}. It is for a city gussing game so you can't give away the city is. Maybe some fun facts. DO NOT INCLUDE ANY LOCATIONS OR AREAS OF THE WORLD. Thank you."},
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

def city_info(city_name, filepath = "./photos-database-scraper.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            local_list_city = data.get("cities", [])
            # Find the city info by name (case-insensitive)
            for city in local_list_city:
                if city.get("city", "").lower() == city_name.lower():
                    return city
            # If not found, return None or an error message
            print(f"City '{city_name}' not found in database.")
            return None
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON file.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


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
                    if guess_lon > city_lon:
                        output = "East"
                    else:
                        output = "West"
                else:
                    if guess_lat > city_lat:
                        output = "North"
                    else:
                        output = "South"
            elif mode == "cardinal":
                if guess_lat > city_lat:
                    output = "North"
                else:
                    output = "South"
            else:
                if abs((guess_lon + guess_lat) - (city_lon + city_lat)) < 20:
                    output = "Yellow"
                else:
                    output = "Grey"

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
                   output = "Yellow"
            else:
                output = "Grey"

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
        # Add new city if not present
        if "cities" not in data or not isinstance(data["cities"], list):
            data["cities"] = []
        if not any(c.get('city', '').lower() == city_info['city'].lower() for c in data['cities']):
            data["cities"].append(city_info)
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        # else: already present, do nothing
    # else: error or not found, do nothing

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
    
def write_ai_data(city, data, filepath="photos-database-scraper.json"):
    with open(filepath, "r", encoding="utf-8") as file:
        data_json = json.load(file)
    for i in range(len(data_json["cities"])):
        if data_json["cities"][i]["city"].lower() == city.lower():
            data_json["cities"][i]["ai"] = data
            break
def read_ai_data(city, filepath="photos-database-scraper.json"):
    with open(filepath, "r", encoding="utf-8") as file:
        data_json = json.load(file)
    for i in range(len(data_json["cities"])):
        if data_json["cities"][i]["city"].lower() == city.lower():
            return data_json["cities"][i].get("ai", "")

def logic(real_city, guess, orginal_state):
    new_state = {
        "city": real_city,
        "guesses": orginal_state.get('guesses')
    }

    city_info = get_city_info(real_city)
    if not city_info or (isinstance(city_info, dict) and city_info.get('error')):
        print("No cities in database.")
        return "No Cities In DataBase"
    print(f"City: {city_info.get('city', 'Unknown City')}")

    # Use the guess argument directly
    person_guess = guess
    if not person_guess:
        print("Invalid guess.")
        return "Invalid guess."
    person_guess_normalized = person_guess.lower().replace('city', '').replace('.', '').replace(',', '').strip()
    person_guess_info = city_api(person_guess)
    if not person_guess_info:
        print("Invalid guess info.")
        return "Invalid guess info."
    target_city_normalized = city_info.get('city', '').lower().replace('city', '').replace('.', '').replace(',', '').strip()
    guess_city_normalized = person_guess_info.get('city', '').lower().replace('city', '').replace('.', '').replace(',', '').strip()
    target_country_normalized = city_info.get('country', '').lower().strip()
    guess_country_normalized = person_guess_info.get('country', '').lower().strip()
    print(target_city_normalized)
    def get_state(city_dict):
        components = city_dict.get('components', {})
        return components.get('state', '').lower().strip() if components else ''
    guess_state = get_state(person_guess_info)
    target_state = get_state(city_info)
    if target_country_normalized == 'united states' and guess_country_normalized == 'united states' and guess_state and target_state:
        if guess_state == target_state:
            country_hint = f"{guess_state.title()}, green"
        else:
            country_hint = f"{guess_state.title()}, grey"
    elif guess_country_normalized == target_country_normalized:
        country_hint = f"{person_guess_info.get('country')}, green"
    else:
        if person_guess_info.get('country') and city_info.get('country'):
            relative_distance_country = compare_country(person_guess_info.get('country'), city_info.get('country'))
            if relative_distance_country == "Yellow":
                country_hint = f"{person_guess_info.get('country')}, yellow"
            else:
                country_hint = f"{person_guess_info.get('country')}, grey"
        else:
            country_hint = "Unknown"
    if guess_city_normalized == target_city_normalized:
        print(f"Correct! You win! {country_hint}")
        return(f"Correct! You win! {country_hint}")
    direction = compare_city(guess, city_info.get('city'), "dir")
    relative_distance_city = compare_city(guess, city_info.get('city'), "cardinal")
    to_add = f"{country_hint}, {person_guess_info.get('city')}, {relative_distance_city}, {direction}"
    print(to_add)

    # Split the to_add string at ', ' and append as a list of values
    to_add_list = to_add.split(', ')
    if isinstance(new_state["guesses"], list):
        new_state["guesses"].append(to_add_list)
    else:
        new_state["guesses"] = [to_add_list]

def get_commons_images(category_url, max_images=10):
    """
    Scrape image URLs from a Wikimedia Commons category page using the Wikimedia API.
    Args:
        category_url (str): The URL of the Wikimedia Commons category page.
        max_images (int): Maximum number of image URLs to return.
    Returns:
        list: List of image URLs.
    """
    import re
    import urllib.parse
    # Extract category name from URL
    match = re.search(r"Category:(.+)", category_url)
    if not match:
        print("Invalid category URL")
        return []
    category_name = match.group(1)
    category_name = urllib.parse.unquote(category_name.replace(' ', '_'))
    api_url = (
        "https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers"
        f"&gcmtitle=Category:{category_name}&gcmtype=file&gcmlimit={max_images}"
        "&prop=imageinfo&iiprop=url&format=json"
    )
    response = requests.get(api_url)
    data = response.json()
    images = []
    pages = data.get('query', {}).get('pages', {})
    for page in pages.values():
        imageinfo = page.get('imageinfo', [])
        if imageinfo:
            images.append(imageinfo[0]['url'])
    return images

def get_author(image_url):
    """
    Get the author of an image from its Wikimedia Commons File page.
    Args:
        image_url (str): The URL of the image.
    Returns:
        str: Author of the image.
    """
    import urllib.parse
    # Extract the filename from the image URL
    filename = image_url.split('/')[-1]
    # Some images have query params, remove them
    filename = filename.split('?')[0]
    # Build the File page URL
    file_page_url = f"https://commons.wikimedia.org/wiki/File:{urllib.parse.quote(filename)}"
    response = requests.get(file_page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    author_tag = soup.find('a', {'class': 'mw-userlink'})
    if author_tag:
        return author_tag.text
    return "Unknown Author"

def get_author_and_license(image_url):
    """
    Get the author and license of an image from its Wikimedia Commons File page.
    Args:
        image_url (str): The URL of the image.
    Returns:
        tuple: (author, license)
    """
    import urllib.parse
    # Extract the filename from the image URL
    filename = image_url.split('/')[-1]
    filename = filename.split('?')[0]
    file_page_url = f"https://commons.wikimedia.org/wiki/File:{urllib.parse.quote(filename)}"
    response = requests.get(file_page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Author
    author_tag = soup.find('a', {'class': 'mw-userlink'})
    author = author_tag.text if author_tag else "Unknown Author"
    # License
    license_tag = soup.find('a', class_='external free')
    if not license_tag:
        # Try to find license in a div with class 'licensetpl'
        license_div = soup.find('div', class_='licensetpl')
        license = license_div.text.strip() if license_div else "Unknown License"
    else:
        license = license_tag.text.strip()
    return author, license

def get_author_and_license_api(image_url):
    """
    Get the author and license of an image from its Wikimedia Commons File page using the Wikimedia API.
    Args:
        image_url (str): The URL of the image.
    Returns:
        tuple: (author, license)
    """
    import urllib.parse
    import re
    global nolicenses, noauthor
    # Extract the filename from the image URL
    filename = image_url.split('/')[-1]
    filename = filename.split('?')[0]

    # Use the API to get image metadata
    api_url = (
        "https://commons.wikimedia.org/w/api.php?action=query&titles=File:" + urllib.parse.quote(filename) +
        "&prop=imageinfo&iiprop=extmetadata|user&format=json"
    )
    response = requests.get(api_url)
    data = response.json()
    pages = data.get('query', {}).get('pages', {})
    for page in pages.values():
        imageinfo = page.get('imageinfo', [{}])[0]
        extmetadata = imageinfo.get('extmetadata', {})
        # Try Artist, then Credit, then Attribution
        author = extmetadata.get('Artist', {}).get('value', '')
        if not author:
            author = extmetadata.get('Credit', {}).get('value', '')
        if not author:
            author = extmetadata.get('Attribution', {}).get('value', '')
        # Remove HTML tags from author if present
        from bs4 import BeautifulSoup
        author = BeautifulSoup(author, 'html.parser').get_text()
        # Clean up author string
        author = re.sub(r'\{\{.*?\}\}', '', author)  # Remove templates
        author = re.sub(r'User:|user:', '', author)      # Remove User: prefix
        author = re.sub(r'\[.*?\]', '', author)        # Remove brackets
        author = author.replace('\n', ' ').replace('\r', ' ').strip(' ,;:-')
        # Fallback to uploader if still empty
        if not author or author.lower() == 'unknown':
            uploader = imageinfo.get('user', '')
            if uploader:
                author = f"Uploader: {uploader}"
            else:
                author = 'Unknown Author'
                # noauthor += 1
        # License: Try LicenseShortName, then UsageTerms, then Permission, then LicenseUrl
        license = extmetadata.get('LicenseShortName', {}).get('value', '')
        if not license:
            license = extmetadata.get('UsageTerms', {}).get('value', '')
        if not license:
            license = extmetadata.get('Permission', {}).get('value', '')
        if not license:
            license = extmetadata.get('LicenseUrl', {}).get('value', '')
        license = BeautifulSoup(license, 'html.parser').get_text().strip()
        if not license:
            license = 'Unknown License'
            # nolicenses +=1
        return author, license
    return "Unknown Author", "Unknown License"

def search_commons_images_by_name(city_name, max_images=1):
    """
    Search Wikimedia Commons for images with the city name in the title.
    Args:
        city_name (str): The name of the city to search for.
        max_images (int): Maximum number of image URLs to return.
    Returns:
        list: List of image URLs.
    """
    api_url = (
        "https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search"
        f"&gsrsearch=file:{city_name}&gsrlimit={max_images}&prop=imageinfo&iiprop=url"
    )
    response = requests.get(api_url)
    data = response.json()
    images = []
    pages = data.get('query', {}).get('pages', {})
    for page in pages.values():
        imageinfo = page.get('imageinfo', [])
        if imageinfo:
            images.append(imageinfo[0]['url'])
    return images

# if True:
if __name__ == "__main__":
    nolicenses = 0
    noauthor = 0
    author = ''
    url = ''
    with open('photos-database-scraper.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    categories = [city['city'] for city in data.get('cities', []) if 'city' in city]
    updated_cities = []
    for city in categories:
        city_category = city.replace(' ', '_')
        category_url = f"https://commons.wikimedia.org/wiki/Category:{city_category}"
        image_urls = get_commons_images(category_url, 50)
        # Only keep JPEG images
        image_urls = [url for url in image_urls if url.lower().endswith('.jpg') or url.lower().endswith('.jpeg')]
        if not image_urls:
            image_urls = search_commons_images_by_name(city, 10)
            image_urls = [url for url in image_urls if url.lower().endswith('.jpg') or url.lower().endswith('.jpeg')]
            if not image_urls:
                print(f"No JPEG images found for {city}")
                continue
        found = False
        found_author = False
        found_license = False
        last_url = image_urls[-1]
        for url in reversed(image_urls):
            author, license = get_author_and_license_api(url)
            if author != 'Unknown Author':
                found_author = True
            if license != 'Unknown License':
                found_license = True
            if license != 'Unknown License' and author != 'Unknown Author':
                print(f"{city}: {url}, Photo by {author} / Wikimedia Commons, {license}")
                found = True
                break
        if not found:
            # Pick the last image and print with 'Unknown License' or 'Unknown Author'
            author, license = get_author_and_license_api(last_url)
            print(f"{city}: {last_url}, Photo by {author} / Wikimedia Commons, Unknown License")
        if not found_author:
            noauthor += 1
        if not found_license:
            nolicenses += 1
        # Get city info (country, latitude, longitude)
        city_info = get_city_info(city)
        country = city_info.get('country', 'Unknown')
        latitude = city_info.get('latitude', None)
        longitude = city_info.get('longitude', None)
        # Format credit string
        credit = f"Photo by {author} / Wikimedia Commons, {license}"
        city_entry = {
            'city': city,
            'country': country,
            'latitude': latitude,
            'longitude': longitude,
            'image': url if found else last_url,
            'credit': credit,
            'ai': ""
        }
        updated_cities.append(city_entry)
    print('Cities with no author:', noauthor)
    print('Cities with no license:', nolicenses)
    # Save results to JSON
    with open('photos-database-scraper.json', 'w', encoding='utf-8') as file:
        json.dump({'cities': updated_cities}, file, ensure_ascii=False, indent=4)
    print("Done!")

if __name__ == "__main__":
    state = {
    'city': 'las vagas',
    'guesses': [['boston', 'red', 'usa', 'green', 'west']]
        }
    print(state)
    logic("Boston", "New York", state)
    print("After logic")
    print(state)
    print("Done!")