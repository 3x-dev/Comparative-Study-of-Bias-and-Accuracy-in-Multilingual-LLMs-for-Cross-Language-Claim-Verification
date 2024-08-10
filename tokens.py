import json

# Load the JSON data from a file
with open('JSON Files/english.json', 'r') as file:
    data = json.load(file)

# Extract and print all claims
claims = [entry['claim'] for entry in data]
for claim in claims:
    print(claim)
