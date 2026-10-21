from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from src.validators import validate_generated_code


class AgentState(TypedDict):
    spec_content: str
    generated_code: str
    validation_errors: List[str]
    iterations: int


def architect_node(state: AgentState) -> AgentState:
    code = "def handler() -> dict:\n    return {'status': 'ok'}\n"
    return {**state, "generated_code": code, "iterations": state["iterations"] + 1}


def verifier_node(state: AgentState) -> AgentState:
    errors = validate_generated_code(state["generated_code"], state["spec_content"])
    return {**state, "validation_errors": errors}


def should_continue(state: AgentState) -> str:
    if not state["validation_errors"] or state["iterations"] >= 3:
        return END
    return "architect"


workflow = StateGraph(AgentState)
workflow.add_node("architect", architect_node)
workflow.add_node("verifier", verifier_node)
workflow.set_entry_point("architect")
workflow.add_edge("architect", "verifier")
workflow.add_conditional_edges("verifier", should_continue)

sdd_app = workflow.compile()

if __name__ == "__main__":
    with open("specs/user-service.openapi.yaml", "r", encoding="utf-8") as f:
        spec = f.read()
    result = sdd_app.invoke({
        "spec_content": spec,
        "generated_code": "",
        "validation_errors": [],
        "iterations": 0,
    })
    print("Final Verified Code:\n", result["generated_code"])
