import csv
import json
import re
from googletrans import Translator

# Initialize the translator
translator = Translator()

# File paths
csv_file_path = 'indo_aryan_gpt-4o_direct_inference.csv'
json_file_path = '../../JSON Files/indo_aryan.json'

# Read CSV file
csv_data = []
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        csv_data.append(row)

# Function to extract final answer from output column
def extract_final_answer(output):
    match = re.search(r'चूड़ांत उत्तर: (.*?)$', output) or \
            re.search(r'अंतिम उत्तर: (.*?)$', output) or \
            re.search(r'ਚੂੜਾਂਤ ਜਵਾਬ: (.*?)$', output) or \
            re.search(r'ચૂડાંત જવાબ: (.*?)$', output) or \
            re.search(r'चूड़ांत उत्तर: (.*?)$', output)
    if match:
        return match.group(1).strip()
    return None

# Function to translate text to English
def translate_to_english(text):
    if text:
        translation = translator.translate(text, dest='en')
        return translation.text
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

# Compare final_answer and label
for row in csv_data:
    claim = row['claim']
    output = row['output']
    correct = row['correct']
    
    final_answer = extract_final_answer(output)
    translated_final_answer = translate_to_english(final_answer)
    
    matching_claim = find_matching_claim(claim, json_data)
    
    if matching_claim:
        json_label = matching_claim['label']
        comparison = (translated_final_answer == json_label)
        result = {
            'claim': claim,
            'final_answer': final_answer,
            'translated_final_answer': translated_final_answer,
            'json_label': json_label,
            'correct': correct,
            'comparison': comparison
        }
    else:
        result = {
            'claim': claim,
            'final_answer': final_answer,
            'translated_final_answer': translated_final_answer,
            'json_label': None,
            'correct': correct,
            'comparison': False
        }
    
    # Print comparison result
    print(f"Claim: {result['claim']}")
    print(f"Final Answer: {result['final_answer']}")
    print(f"Translated Final Answer: {result['translated_final_answer']}")
    print(f"JSON Label: {result['json_label']}")
    print(f"Correct: {result['correct']}")
    print(f"Comparison: {result['comparison']}")
    print('-' * 40)