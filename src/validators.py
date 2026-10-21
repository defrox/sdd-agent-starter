import ast
import yaml
from typing import List


def extract_required_operations(spec_yaml: str) -> List[str]:
    """Extracts all operationId defined in the OpenAPI specification."""
    spec = yaml.safe_load(spec_yaml)
    operations: List[str] = []
    paths = spec.get("paths", {})
    for _, methods in paths.items():
        for _, details in methods.items():
            if isinstance(details, dict) and "operationId" in details:
                operations.append(details["operationId"])
    return operations


def validate_generated_code(code: str, spec_yaml: str) -> List[str]:
    """Validates Python syntax, type annotations, and OpenAPI contract compliance."""
    errors: List[str] = []

    # 1. Syntax validation using AST
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return [f"SyntaxError in generated code: {exc}"]

    # 2. Collect defined functions and check return type annotation
    defined_functions = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            defined_functions[node.name] = node
            if node.returns is None:
                errors.append(f"Typing violation: function '{node.name}' lacks return type annotation.")

    # 3. Verify that each operationId in the contract exists in the code
    required_ops = extract_required_operations(spec_yaml)
    for op in required_ops:
        if op not in defined_functions:
            errors.append(f"Contract violation: missing required operationId '{op}'.")

    return errors
