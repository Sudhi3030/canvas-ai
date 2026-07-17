import json
from typing import Dict, Any, Union
from pydantic import ValidationError
from design_engine.scene_graph.document import Layout

def validate_layout(data: Union[str, Dict[str, Any]]) -> Layout:
    """
    Validates canvas layout data against the Pydantic Layout model.
    Accepts a JSON string or a Python dictionary.
    Returns the parsed Layout object if valid, otherwise raises ValidationError.
    """
    if isinstance(data, str):
        parsed_data = json.loads(data)
    else:
        parsed_data = data
        
    return Layout.model_validate(parsed_data)

def format_validation_error(err: ValidationError) -> str:
    """
    Formats Pydantic ValidationError into a readable, detailed string.
    """
    lines = []
    for error in err.errors():
        loc = " -> ".join(str(p) for p in error["loc"])
        msg = error["msg"]
        lines.append(f"Field: {loc}\nError: {msg}\n")
    return "\n".join(lines)

def generate_layout_schema() -> Dict[str, Any]:
    """
    Generates the complete JSON Schema for the Layout model.
    """
    return Layout.model_json_schema()
