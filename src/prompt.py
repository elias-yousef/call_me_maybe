import json
from pathlib import Path

def setup_dynamic_environment(functions_file_path: Path, user_query: str):
    """
    Reads the schema dynamically. Returns both the super prompt for the AI
    and the list of valid function names for your State Machine.
    """
    
    # 1. Read the JSON file into a Python List of Dictionaries
    with open(functions_file_path, 'r', encoding='utf-8') as f:
        functions_data = json.load(f) # functions_data is now a Python object
        
    # 2. DYNAMIC DISCOVERY: Extract the valid function names automatically.
    # We loop through the data and grab the "name" field from each function.
    valid_function_names = [func["name"] for func in functions_data]
    
    print(f"DEBUG: I dynamically found these allowed functions: {valid_function_names}")
    
    # 3. Format the data for the AI. 
    # json.dumps converts our Python object back into a clean string format.
    # indent=2 makes it readable for the AI.
    schema_string = json.dumps(functions_data, indent=2)
    
    # 4. Build the dynamic prompt. 
    # Notice we don't hardcode fn_add_numbers anywhere in this string!
    prompt = f"""You are a precise system that translates natural language into JSON function calls.
Here is the strict JSON schema for the functions you can use:

{schema_string}

Task: Read the User Request and output a single JSON object specifying the function name and arguments.

User Request: {user_query}
Output: {{"name": \""""

    return prompt, valid_function_names

# --- Test it in your __main__.py ---
# my_prompt, allowed_names = setup_dynamic_environment(
#     Path("data/input/functions_definition.json"), 
#     "Greet shrek"
# )
