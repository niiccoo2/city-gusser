import requests
from bs4 import BeautifulSoup
import json
import sys
sys.path.append('.')
from functions import get_city_info

# Example: Scrape images from a Wikipedia Commons category page

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