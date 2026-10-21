import pytest
from src.validators import validate_generated_code, extract_required_operations
from src.graph import sdd_app

SAMPLE_SPEC = """
openapi: 3.1.0
info:
  title: User Verification Service
  version: 1.0.0
paths:
  /health:
    get:
      operationId: handler
      responses:
        "200":
          description: Service health status
"""


def test_extract_required_operations():
    ops = extract_required_operations(SAMPLE_SPEC)
    assert ops == ["handler"]


def test_valid_contract_passes():
    valid_code = "def handler() -> dict:\n    return {'status': 'ok'}\n"
    errors = validate_generated_code(valid_code, SAMPLE_SPEC)
    assert errors == []


def test_missing_operation_fails():
    invalid_code = "def wrong_name() -> dict:\n    return {'status': 'ok'}\n"
    errors = validate_generated_code(invalid_code, SAMPLE_SPEC)
    assert any("missing required operationId 'handler'" in err for err in errors)


def test_missing_return_type_fails():
    untyped_code = "def handler():\n    return {'status': 'ok'}\n"
    errors = validate_generated_code(untyped_code, SAMPLE_SPEC)
    assert any("lacks return type annotation" in err for err in errors)


def test_end_to_end_sdd_graph():
    result = sdd_app.invoke({
        "spec_content": SAMPLE_SPEC,
        "generated_code": "",
        "validation_errors": [],
        "iterations": 0,
    })
    assert result["validation_errors"] == []
    assert "def handler" in result["generated_code"]
