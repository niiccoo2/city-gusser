import main

cities = main.fetch_cities_from_json()
print(cities)
random_image = main.grab_random_city(cities)
print(random_image)
image = random_image.get('image')
print(image)