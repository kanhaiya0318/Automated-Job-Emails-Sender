from __future__ import annotations
from typing import Literal

__all__ = ["route_next", "route_after_approval"]

def route_next(state) -> Literal["send_email", "others", "scan_next_post", "end"]:
    jc = state.get("job_count", 0)
    jobs = state.get("relevant_jobs", [])
    if jc < len(jobs):
        if jobs[jc].get("is_positive_email"):
            return "send_email"  
        else:
            return "others"
    if state.get("count_scraped_posts", 0) < state.get("total_scraped_posts", 0):
        return "scan_next_post"
    return "end"


def route_after_approval(state) -> Literal["approved", "send_email", "others", "scan_next_post", "end"]:
    if state.get("email_approved"):
        return "approved"
    return route_next(state)