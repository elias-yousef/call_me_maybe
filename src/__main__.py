from typing import Any, Dict
import sys
import argparse
from pydantic import BaseModel
import json


class prompt_validate(BaseModel):
    prompt: str


class function_definition_validate(BaseModel):
    name: str
    description: str
    returns: Dict[str, Any]
    parameters: Dict[str, Any]


def parse_args() -> argparse.Namespace:
    """Configure and parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--functions_definition",
        type=str,
        default="data/input/functions_definition.json"
        )
    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json"
        )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results.json"
        )
    return parser.parse_args()


def load_json_safe(filepath: str) -> Any:
    """Safely load a JSON file using context managers and error handling."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Required file not found at '{filepath}'.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: File '{filepath}' contains invalid JSON. {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error reading '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    args = parse_args()
    functions_data = load_json_safe(args.functions_definition)
    prompts_data = load_json_safe(args.input)
    
    print(f"Successfully loaded {len(functions_data)} functions.")
    print(f"Successfully loaded {len(prompts_data)} prompts.")

    try:
        for i in range(len(prompts_data)):
            prompt_validate(**prompts_data[i])
    except ValueError as e:
        print(f"Data validation failed: {e}")
    try:
        for i in range(len(functions_data)):
            function_definition_validate(**functions_data[i])
    except ValueError as e:
        print(f"Data validation failed: {e}")

if __name__ == "__main__":
    main()
