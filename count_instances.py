import os
import json
from collections import defaultdict

# Path to the directory containing JSON files
directory_path = 'JSON Files'

# Initialize dictionaries to hold the counts
language_counts = defaultdict(int)
label_counts = defaultdict(lambda: defaultdict(int))
total_claims = 0
total_labels = defaultdict(int)

# Iterate through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        file_path = os.path.join(directory_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            for entry in data:
                language = entry['language']
                label = entry['label']
                
                # Increment counts
                language_counts[language] += 1
                label_counts[language][label] += 1
                total_claims += 1
                total_labels[label] += 1

# Print the results
print("Language Counts:")
for language, count in language_counts.items():
    print(f"{language}: {count} claims")

print("\nLabel Counts per Language:")
for language, labels in label_counts.items():
    print(f"\n{language}:")
    for label, count in labels.items():
        print(f"  {label}: {count}")

print("\nTotal Counts:")
print(f"Total Claims: {total_claims}")
for label, count in total_labels.items():
    print(f"Total {label}: {count}")
