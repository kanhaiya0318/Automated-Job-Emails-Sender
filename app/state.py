from typing import TypedDict, Annotated
from operator import add


class state(TypedDict):
    maxposts:int
    apify_output:list[dict]
    apify_filtered_output:list[dict]
    total_scraped_posts:int
    count_scraped_posts:int

    job_scan_output:dict
    relevant_jobs:list[dict]
    irrelevant:list[dict]
    total_relevant_jobs:Annotated[list[dict], add]
    total_irrelevant:Annotated[list[dict], add]
    total_job_scan_output:Annotated[list[dict], add]
    
    post_relevant_count:int   # total jobs relevant jobs in single post
    job_count:int            # how much i done by total relevant jobs in single post

    unique_email:Annotated[list[str], add]
    
    email_approved: bool
    email_subject: str
    email_body: str