from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents.rag_agent import rag_chat
from agents.general_agent import general_chat
from agents.test_agent import test_chat
from agents.architecture_agent import architecture_chat
from agents.codegen_agent import codegen_chat
from agents.pr_review_agent import pr_review_chat
from agents.readme_agent import readme_chat
from agents.issue_agent import issue_chat

class AgentState(TypedDict):
    query: str
    agent_type: str
    response: str


def planner_agent(state: AgentState):
    query = state["query"].lower()
    if (
    "create" in query
    or "generate code" in query
    or "build" in query
    or "implement" in query
    or "add feature" in query
    or "make api" in query
    or "create component" in query
    ):
       agent_type = "codegen"

    if (
        "test" in query
        or "unit test" in query
        or "integration test" in query
        or "pytest" in query
        or "jest" in query
    ):
        agent_type = "test"

    elif (
        "error" in query
        or "bug" in query
        or "traceback" in query
        or "debug" in query
    ):
        agent_type = "debug"

    elif (
        "readme" in query
        or "documentation" in query
        or "document" in query
    ):
        agent_type = "docs"

    elif (
        "review" in query
        or "improve" in query
        or "refactor" in query
    ):
        agent_type = "review"
    
    elif (
    "architecture" in query
    or "system design" in query
    or "project structure" in query
    or "folder structure" in query
    ):
        agent_type = "architecture"

    elif (
        "explain this repo" in query
        or "codebase" in query
        or "architecture" in query
        or "where is" in query
        or "how does" in query
        or "function" in query
        or "file" in query
    ):
        agent_type = "rag"
    elif (
    "pull request" in query
    or "pr review" in query
    or "review this diff" in query
    or "git diff" in query
    or "diff" in query
    ):
        agent_type = "pr_review"

    elif (
    "readme" in query
    or "project summary" in query
    or "github description" in query
    ):
        agent_type = "readme"
    
    elif (
    "issue" in query
    or "bug report" in query
    or "fix bug" in query
    or "root cause" in query
    ):
        agent_type = "issue"

    else:
        agent_type = "general"

    return {
        **state,
        "agent_type": agent_type
    }


def rag_agent(state: AgentState):
    response = rag_chat(state["query"])
    return {**state, "response": response}


def debug_agent(state: AgentState):
    query = f"""
You are a debugging agent.

Use the indexed codebase context if available.
Find the possible bug, explain the root cause, and suggest a fix.

User issue:
{state["query"]}
"""
    response = rag_chat(query)
    return {**state, "response": response}


def docs_agent(state: AgentState):
    query = f"""
You are a documentation agent.

Generate clear developer documentation using the indexed codebase context.

User request:
{state["query"]}
"""
    response = rag_chat(query)
    return {**state, "response": response}


def review_agent(state: AgentState):
    query = f"""
You are a senior code reviewer.

Review the related codebase context and suggest improvements, bugs, security issues, and refactoring ideas.

User request:
{state["query"]}
"""
    response = rag_chat(query)
    return {**state, "response": response}


def test_agent(state: AgentState):
    response = test_chat(state["query"])
    return {**state, "response": response}


def general_agent(state: AgentState):
    response = general_chat(state["query"])
    return {**state, "response": response}


def route_agent(state: AgentState):
    return state["agent_type"]

def architecture_agent(state):
    response = architecture_chat(state["query"])

    return {
        **state,
        "response": response
    }

def codegen_agent(state: AgentState):
    response = codegen_chat(state["query"])
    return {**state, "response": response}

def pr_review_agent(state: AgentState):
    response = pr_review_chat(state["query"])
    return {**state, "response": response}

def readme_agent(state: AgentState):
    response = readme_chat(state["query"])
    return {**state, "response": response}
def issue_agent(state: AgentState):
    response = issue_chat(state["query"])
    return {
        **state,
        "response": response
    }

workflow = StateGraph(AgentState)

workflow.add_node("planner", planner_agent)
workflow.add_node("rag", rag_agent)
workflow.add_node("debug", debug_agent)
workflow.add_node("docs", docs_agent)
workflow.add_node("review", review_agent)
workflow.add_node("test", test_agent)
workflow.add_node("general", general_agent)
workflow.add_node(
    "architecture",
    architecture_agent
)
workflow.add_node("codegen", codegen_agent)
workflow.add_node("pr_review", pr_review_agent)
workflow.add_node("readme", readme_agent)

workflow.add_node(
    "issue",
    issue_agent
)

workflow.set_entry_point("planner")

workflow.add_conditional_edges(
    "planner",
    route_agent,
    {
        "rag": "rag",
        "debug": "debug",
        "docs": "docs",
        "review": "review",
        "test": "test",
        "general": "general",
        "architecture": "architecture",
        "codegen": "codegen",
        "pr_review": "pr_review",
        "readme": "readme",
        "issue": "issue",
    }
)

workflow.add_edge("rag", END)
workflow.add_edge("debug", END)
workflow.add_edge("docs", END)
workflow.add_edge("review", END)
workflow.add_edge("test", END)
workflow.add_edge("general", END)
workflow.add_edge(
    "architecture",
    END
)
workflow.add_edge("codegen", END)
workflow.add_edge("pr_review", END)
workflow.add_edge("readme", END)
workflow.add_edge("issue", END)

app_graph = workflow.compile()


def run_graph(query: str):
    result = app_graph.invoke({
        "query": query,
        "agent_type": "",
        "response": ""
    })

    return result