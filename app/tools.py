from typing import Dict, Any

def add_numbers(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Add two numbers from inputs."""
    a = float(inputs.get("a", 0))
    b = float(inputs.get("b", 0))
    return {"result": a + b}

def to_uppercase(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Uppercase a string input 'text'."""
    text = str(inputs.get("text", ""))
    return {"result": text.upper()}
