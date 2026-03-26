import json

# 1. Load your original data
with open('more.json', 'r') as f:
    original_data = json.load(f)

promptfoo_tests = []

for item in original_data:
    # Identify which choice (A, B, C, or D) is the correct one
    answer_letter = item.get('answer') # e.g., "B"
    choice_key = f"choice_{answer_letter}" # creates "choice_B"
    
    # Extract the actual text for the correct answer
    ground_truth_text = item.get(choice_key, "")

    # Create the Promptfoo test case
    test_case = {
        "vars": {
            # This 'unpacks' all original fields (id, domain, difficulty, etc.)
            **item,
            # This adds/overwrites the specific ground_truth text for the assertion
            "ground_truth": ground_truth_text
        },
        "assert": [
            {
                "type": "similar",
                "value": ground_truth_text,
                "threshold": 0.8
            }
        ]
    }
    promptfoo_tests.append(test_case)

# 2. Save the new format
with open('tests.json', 'w') as f:
    json.dump(promptfoo_tests, f, indent=2)

print(f"Successfully created tests.json with {len(promptfoo_tests)} cases!")
