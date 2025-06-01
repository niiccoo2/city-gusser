import json

# Replace with your actual JSON file path
json_file_path = r"C:\Users\Nico\Documents\programing\python\city-gusser\photos\photos-database.json"

def main():
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        cities = data.get("cities", [])
        if not cities:
            print("No cities found in JSON.")
            return

        for city in cities:
            print(f"City: {city.get('city')}")
            print(f"Country: {city.get('country')}")
            print(f"Coordinates: ({city.get('lat')}, {city.get('lon')})")
            print(f"Image URL: {city.get('image')}")
            print(f"Credit: {city.get('credit')}")
            print("-" * 40)

    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
