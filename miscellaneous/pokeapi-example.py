
# This code is an example of how to connect to the PokeAPI
# As documented here: https://pokeapi.co/

# Import requests, for calling the API
import requests
# Import pretty print, for displaying JSON in a more readable way
from pprint import pprint

# Call the pokemon API
response = requests.get("https://pokeapi.co/api/v2/pokemon-color/red")

# Check that the response code is 200 (what we expect for a good request)
if response.status_code != 200:
    print("Unexpected status code:", response.status_code)
    exit()

# Parse JSON to python dictionary and print
data = response.json()
pprint(data)

# Example for how we might loop over the data
for pokemon in data["pokemon_species"]:
    print(pokemon["name"])

# Ideas:
# 1. Build a team of six grass type pokemon
# 2. Select four moves for each of the pokemon
# 3. Make sure none of the moves are shared
# 4. Make sure none of the pokemon are related by evolution
