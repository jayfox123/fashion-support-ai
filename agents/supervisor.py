
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from agents.order_agent import OrderAgent
from agents.query_agent import QueryAgent
from agents.recommendation_agent import RecommendationAgent
from agents.returns_agent import ReturnsAgent
from agents.escalation_agent import EscalationAgent

class AgentState(TypedDict):
    message: str
    context: dict
    response: str
    agent_used: str

order_agent = OrderAgent()
query_agent = QueryAgent()
recommendation_agent = RecommendationAgent()
returns_agent = ReturnsAgent()
escalation_agent = EscalationAgent()

def route_message(state: AgentState) -> str:
    message = state["message"].lower()
    history = state["context"].get("history", [])
    
    last_agent = state["context"].get("last_agent", None)

    all_text = message

    for turn in history:
        all_text += " " + turn.get("content", "").lower()

    if escalation_agent.should_escalate(message):
        return "escalation"

    if any(word in message for word in [
        "order", "tracking", "shipped", "delivery",
        "where is my", "status", "package", "ord-", "ord"
    ]):
        return "order"

    if any(word in message for word in [
        "return", "refund", "exchange", "send back",
        "money back", "swap"
    ]):
        return "returns"

    if any(word in all_text for word in [
        "recommend", "suggest", "looking for", "find me",
        "what should i wear", "outfit", "style", "size",
        "color", "dress", "shirt", "shoes", "jacket"
    ]):
        return "recommendation"

    if last_agent and last_agent not in ["query"]:
        return last_agent
    return "query"

def order_node(state: AgentState) -> AgentState:
    response = order_agent.handle(state["message"], state["context"])
    return {**state, "response": response, "agent_used": "order_agent"}

def query_node(state: AgentState) -> AgentState:
    response = query_agent.handle(state["message"], state["context"])
    return {**state, "response": response, "agent_used": "query_agent"}

def recommendation_node(state: AgentState) -> AgentState:
    response = recommendation_agent.handle(state["message"], state["context"])
    return {**state, "response": response, "agent_used": "recommendation_agent"}

def returns_node(state: AgentState) -> AgentState:
    response = returns_agent.handle(state["message"], state["context"])
    return {**state, "response": response, "agent_used": "returns_agent"}

def escalation_node(state: AgentState) -> AgentState:
    response = escalation_agent.handle(state["message"], state["context"])
    return {**state, "response": response, "agent_used": "escalation_agent"}

workflow = StateGraph(AgentState)

workflow.add_node("order", order_node)
workflow.add_node("query", query_node)
workflow.add_node("recommendation", recommendation_node)
workflow.add_node("returns", returns_node)
workflow.add_node("escalation", escalation_node)

workflow.set_conditional_entry_point(
    route_message,
    {
        "order": "order",
        "query": "query",
        "recommendation": "recommendation",
        "returns": "returns",
        "escalation": "escalation"
    }
)

workflow.add_edge("order", END)
workflow.add_edge("query", END)
workflow.add_edge("recommendation", END)
workflow.add_edge("returns", END)
workflow.add_edge("escalation", END)

supervisor = workflow.compile()

def handle_customer_message(message: str, context: dict = {}) -> dict:
    result = supervisor.invoke({
        "message": message,
        "context": context,
        "response": "",
        "agent_used": ""
    })
    return {
        "response": result["response"],
        "agent_used": result["agent_used"]
    }