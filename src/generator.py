from llm_sdk import Small_LLM_Model as LLMS
import numpy as np
import json


def json_format_next_ids(input_ids: list[int], id_to_token: dict) -> list[int]:
    pass


def generate_text(prompt: str, MAX_TOKEN: int = 30):
    model = LLMS()
    raw_encoded = model.encode(prompt)
    voc_path = model.get_path_to_vocab_file()

    with open(voc_path, 'r', encoding="utf-8") as file:
        json_data = json.load(file)
        id_to_token = {value: key for key, value in json_data.items()}

    if hasattr(raw_encoded, "tolist"):
        input_ids = raw_encoded.tolist()[0]
    else:
        input_ids = raw_encoded[0]

    for _ in range(MAX_TOKEN):
        logits = model.get_logits_from_input_ids(input_ids)
        next_input_id = int(np.argmax(logits))
        input_ids.append(next_input_id)
        new_text = model.decode([next_input_id])
        print(new_text, end="", flush=True)
    print("\n")

if __name__ == "__main__":
    generate_text("hi how are you")

