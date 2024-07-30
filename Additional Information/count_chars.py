import os
import json

def count_claim_characters_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    total_characters = sum(len(item['claim']) for item in data if 'claim' in item)
    return total_characters

def count_claim_characters_in_folder(folder_path):
    total_characters_per_file = {}
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            total_characters = count_claim_characters_in_file(file_path)
            total_characters_per_file[filename] = total_characters

    return total_characters_per_file

# Folder containing the JSON files
folder_path = 'JSON Files'

# Get the total characters in claims for each file
total_characters_per_file = count_claim_characters_in_folder(folder_path)

# Print the results
for filename, total_characters in total_characters_per_file.items():
    print(f"{filename}: {total_characters} characters in claims")

# Save results to a JSON file
output_file_path = 'claim_characters_summary.json'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(total_characters_per_file, output_file, ensure_ascii=False, indent=4)

print(f"Summary saved to {output_file_path}")
