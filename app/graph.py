from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from app.state import state
from app.nodes import *
from app.routers import *

__all__ = ["build_graph"]


route_map = {"send_email": "email_draft", "others": "others",
                "scan_next_post": "scan_job_posts", "end": END}

def build_graph():
    g = StateGraph(state)
    memory = InMemorySaver()

    #node
    g.add_node("apify_data_scrap", apify_data_scrap)
    g.add_node("filter_apify_output", filter_apify_output)
    g.add_node("scan_job_posts", scan_job_posts)
    g.add_node("find_relevant_jobs",find_relevant_jobs)
    g.add_node("email_draft", email_draft)
    g.add_node("email_send", email_send)
    g.add_node("others", others)


    #edge
    g.add_edge(START, "apify_data_scrap")
    g.add_edge("apify_data_scrap", "filter_apify_output")
    g.add_edge("filter_apify_output", "scan_job_posts")
    g.add_edge("scan_job_posts", "find_relevant_jobs")
    g.add_edge("email_draft", "email_send")

    g.add_conditional_edges("find_relevant_jobs", route_next, route_map)
    g.add_conditional_edges("others", route_next, route_map)
    g.add_conditional_edges("email_send", route_next, route_map)

    return g.compile(checkpointer=memory)