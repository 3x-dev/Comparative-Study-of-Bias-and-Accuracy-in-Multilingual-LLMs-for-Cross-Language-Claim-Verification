import csv
import json
import re

# File paths
csv_file_path = 'kartvelian_llama-3.1-70b-versatile_direct_inference.csv'
json_file_path = '../../JSON Files/kartvelian.json'
output_json_path = 'kartvelian_llama-3.1-70b-versatile_direct_inference_summary.json'

# Mapping dictionary for the labels
label_mapping = {
    "მართალი": "true",
    "ძირითადად მართალია": "mostly true",
    "ნახევრად მართალია": "half true",
    "ძირითადად მცდარი": "mostly false",
    "მცდარი": "false"
}


# Read CSV file
csv_data = []
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        csv_data.append(row)

# Function to extract final answer from output column
def extract_final_answer(output):
    patterns = [
        r'საბოლოო პასუხი:(.*?)$',
    ]
    for pattern in patterns:
        match = re.search(pattern, output)
        if match:
            return match.group(1).strip()
    return None

# Function to clean the extracted text
def clean_text(text):
    if text:
        text = re.sub(r'[„“":\'"“”]', '', text)  # Remove special characters
        return text.strip()
    return None

# Read JSON file
with open(json_file_path, 'r', encoding='utf-8') as jsonfile:
    json_data = json.load(jsonfile)

# Function to find matching claim in JSON
def find_matching_claim(claim, json_data):
    for item in json_data:
        if item['claim'] == claim:
            return item
    return None

# Initialize results structure
results = {
    "correct": 0,
    "wrong": 0,
    "inconclusive": 0,
    "total": 0,
    "languages": {
        "ka": {"correct": 0, "wrong": 0, "inconclusive": 0, "total": 0},
    }
}

# Function to write results to JSON file incrementally
def write_results_to_json(results, output_json_path):
    with open(output_json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(results, jsonfile, ensure_ascii=False, indent=4)

# Compare final_answer and label
for row in csv_data:
    claim = row['claim']
    output = row['output']
    language = row['language']
    correct = row['correct']
    
    final_answer = extract_final_answer(output)
    comparison = None
    matching_claim = None

    if final_answer is None:
        results["inconclusive"] += 1
        results["languages"][language]["inconclusive"] += 1
    else:
        cleaned_final_answer = clean_text(final_answer)
        mapped_final_answer = label_mapping.get(cleaned_final_answer, None)
        
        matching_claim = find_matching_claim(claim, json_data)
        
        if matching_claim:
            json_label = matching_claim['label']
            comparison = (mapped_final_answer == json_label)
            
            if comparison:
                results["correct"] += 1
                results["languages"][language]["correct"] += 1
            else:
                results["wrong"] += 1
                results["languages"][language]["wrong"] += 1
        else:
            results["inconclusive"] += 1
            results["languages"][language]["inconclusive"] += 1

    results["total"] += 1
    results["languages"][language]["total"] += 1

    # Write results to JSON file incrementally
    write_results_to_json(results, output_json_path)

    # Print comparison result
    print(f"Claim: {claim}")
    print(f"Final Answer: {final_answer}")
    print(f"Cleaned Final Answer: {cleaned_final_answer if final_answer else 'N/A'}")
    print(f"Mapped Final Answer: {mapped_final_answer if final_answer else 'N/A'}")
    if matching_claim:
        print(f"JSON Label: {matching_claim['label']}")
    else:
        print("JSON Label: None")
    print(f"Correct: {correct}")
    print(f"Comparison: {comparison if final_answer and matching_claim else 'No matching claim or inconclusive'}")
    print('-' * 40)

print(f"Results have been written to {output_json_path}")
