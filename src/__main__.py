import sys
import numpy as np
from llm_sdk import Small_LLM_Model
from pathlib import Path
from src.prompt import setup_dynamic_environment

def generate_text(prompt: str, MAX_TOKEN: int = 20):
    model = Small_LLM_Model()
    raw_encoded = model.encode(prompt)

    if hasattr(raw_encoded, "tolist"):
        input_ids = raw_encoded.tolist()[0]
    else:
        input_ids = raw_encoded[0]
    print(f"\nPrompt: '{prompt}'")
    for _ in range(MAX_TOKEN):
        logits = model.get_logits_from_input_ids(input_ids)
        next_input_id = int(np.argmax(logits))
        input_ids.append(next_input_id)
        new_text = model.decode([next_input_id])
        print(new_text, end="", flush=True)
    print("\n")

# --- Test it in your __main__.py ---
my_prompt, allowed_names = setup_dynamic_environment(
    Path("data/input/functions_definition.json"), 
    "Greet shrek" )
generate_text("what is 2 + 2")