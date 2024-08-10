import csv
import json
import re

# File paths
csv_file_path = 'indo_aryan_gpt-4o-mini_direct_inference.csv'
json_file_path = '../../JSON Files/indo_aryan.json'
output_json_path = 'indo_aryan_gpt-4o-mini_direct_inference_summary.json'

# Mapping dictionary for the labels
label_mapping = {
    "सत्य": "true",
    "अधिकांशतः सत्य": "mostly true",
    "आधा सत्य": "half true",
    "अधिकांशतः असत्य": "mostly false",
    "असत्य": "false",
    "সত্য": "true",
    "অধিকাংশ সত্য": "mostly true",
    "অর্ধসত্য": "half true",
    "অধিকাংশ মিথ্যা": "mostly false",
    "মিথ্যা": "false",
    "ਸੱਚ": "true",
    "ਜਿਆਦਾਤਰ ਸੱਚ": "mostly true",
    "ਅੱਧਾ ਸੱਚ": "half true",
    "ਜਿਆਦਾਤਰ ਝੂਠ": "mostly false",
    "ਝੂਠ": "false",
    "સત્ય": "true",
    "મોટાભાગનું સત્ય": "mostly true",
    "અડધું સત્ય": "half true",
    "મોટાભાગનું ખોટું": "mostly false",
    "ખોટું": "false",
    "अंतिम उत्तर: सत्य": "true",
    "अंतिम उत्तर: अधिकांशतः सत्य": "mostly true",
    "अंतिम उत्तर: आधा सत्य": "half true",
    "अंतिम उत्तर: अधिकांशतः असत्य": "mostly false",
    "अंतिम उत्तर: असत्य": "false",
    "চূড়ান্ত উত্তর: সত্য": "true",
    "চূড়ান্ত উত্তর: অধিকাংশ সত্য": "mostly true",
    "চূড়ান্ত উত্তর: অর্ধসত্য": "half true",
    "চূড়ান্ত উত্তর: অধিকাংশ মিথ্যা": "mostly false",
    "চূড়ান্ত উত্তর: মিথ্যা": "false",
    "ਅੰਤਿਮ ਜਵਾਬ: ਸੱਚ": "true",
    "ਅੰਤਿਮ ਜਵਾਬ: ਜਿਆਦਾਤਰ ਸੱਚ": "mostly true",
    "ਅੰਤਿਮ ਜਵਾਬ: ਅੱਧਾ ਸੱਚ": "half true",
    "ਅੰਤਿਮ ਜਵਾਬ: ਜਿਆਦਾਤਰ ਝੂਠ": "mostly false",
    "ਅੰਤਿਮ ਜਵਾਬ: ਝੂਠ": "false",
    "અંતિમ જવાબ: સત્ય": "true",
    "અંતિમ જવાબ: મોટાભાગનું સત્ય": "mostly true",
    "અંતિમ જવાબ: અડધું સત્ય": "half true",
    "અંતિમ જવાબ: મોટાભાગનું ખોટું": "mostly false",
    "અંતિમ જવાબ: ખોટું": "false"
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
        r'अंतिम उत्तर:(.*?)$',
        r'চূড়ান্ত উত্তর:(.*?)$',
        r'ਅੰਤਿਮ ਜਵਾਬ:(.*?)$',
        r'અંતિમ જવાબ:(.*?)$'
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
        "hi": {"correct": 0, "wrong": 0, "inconclusive": 0, "total": 0},
        "bn": {"correct": 0, "wrong": 0, "inconclusive": 0, "total": 0},
        "pa": {"correct": 0, "wrong": 0, "inconclusive": 0, "total": 0},
        "gu": {"correct": 0, "wrong": 0, "inconclusive": 0, "total": 0},
        "mr": {"correct": 0, "wrong": 0, "inconclusive": 0, "total": 0}
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
