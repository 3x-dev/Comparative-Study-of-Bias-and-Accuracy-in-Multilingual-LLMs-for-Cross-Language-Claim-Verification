import os
import json
from collections import defaultdict

def count_labels(directory):
    label_counts = defaultdict(lambda: defaultdict(int))
    
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for entry in data:
                    language = entry.get('language')
                    label = entry.get('label')
                    if language and label:
                        label_counts[language][label] += 1
    
    return label_counts

def main():
    directory = 'JSON Files'  # replace with your directory path
    results = count_labels(directory)
    
    for language, labels in results.items():
        print(f"Language: {language}")
        for label, count in labels.items():
            print(f"  {label}: {count}")

if __name__ == "__main__":
    main()
