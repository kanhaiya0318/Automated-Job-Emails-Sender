from __future__ import annotations

import os
import json
import base64
import mimetypes
from email.message import EmailMessage
from apify_client import ApifyClient

from config import settings
from app.utils.node_service import b
from app.prompts import job_extraction_chain
from app.schemas import PostExtraction
from app.utils.gmail_service import get_gmail_service
from app.utils.templates import *


__all__ = [
    "apify_data_scrap",
    "filter_apify_output",
    "scan_job_posts",
    "find_relevant_jobs",
    "email_draft",
    "email_send",
    "others",
]


# first Node 
def apify_data_scrap(state):
    if settings.DRY_RUN_APIFY:
        return {"apify_output":b}
    
    # Initialize the ApifyClient with your API token
    client = ApifyClient(settings.APIFY_API_TOKEN)

    # Prepare the Actor input
    run_input = {
        "searchQueries": settings.SEARCHQUERY,
        "maxPosts": state.get("maxposts", 5),
        "sortBy": settings.SORTBY,
        "postedLimit": settings.POSTEDLIMIT,
        "profileScraperMode": "short",
        "startPage": 1,
        "scrapeReactions": False,
        "reactionsProfileScraperMode": "short",
        "postNestedReactions": False,
        "scrapeComments": False,
        "commentsProfileScraperMode": "short",
        "postNestedComments": False,
    }
    try:
        run = client.actor("buIWk2uOUzTmcLsuB").call(run_input=run_input)
        posts = list(client.dataset(run.default_dataset_id).iterate_items())
    except Exception as e:
        print(f"[apify_data_scrap] node fail : {e}")

    return {"apify_output":posts}



# second Node:
def clean_links(attrs):
    seen, out = set(), []
    for a in attrs:
        val = (a.get("textLink") or "").strip()
        if val.lower().startswith("mailto:"):
            val = val[len("mailto:"):].strip()
        if val and val not in seen:
            seen.add(val)
            out.append(val)
    return out

def filter_apify_output(state):
    posts = state.get("apify_output",[])
    dataset = []
    for post in posts:
        data = {
            "data_type": post.get("type", ""),
            "query_sort_by": post.get("query", {}).get("sortBy", ""),
            "search_query": post.get("query",{}).get("search",""),
            "post_how_long": post.get("postedAt", {}).get("postedAgoShort", ""),
            "post_time": post.get("postedAt", {}).get("date", ""),
            "content": post.get("content", ""),
            "post_url": post.get("linkedinUrl", ""),
            "auther_type": post.get("author", {}).get("type", ""),
            "auther_id": post.get("author", {}).get("publicIdentifier", ""),
            "auther_name": post.get("author", {}).get("name", ""),
            "auther_url": post.get("author", {}).get("linkedinUrl", ""),
            "links_emails": clean_links(post.get("contentAttributes", [])),        
        }
        dataset.append(data)
    total_count = len(dataset)
    return {"apify_filtered_output":dataset, "total_scraped_posts":total_count}



# third Node : 
def scan_job_posts(state):
    post_count = state.get("count_scraped_posts",0)
    total_posts = state.get("total_scraped_posts", 0)
    if  post_count < total_posts:
        filtered_job_post = state.get("apify_filtered_output", "")
 
        post = filtered_job_post[post_count]
        try:
            out = job_extraction_chain.invoke({
                "content":post["content"],
                "links":post["links_emails"],
                "post_url":post["post_url"],
            })
        except Exception as e:
            print(f"[SCAN FAILED] post {post_count + 1} ({post['post_url']}): {e}")
            out = PostExtraction(is_hiring_post=False, jobs=[])
 
        return {
            "job_scan_output":out.model_dump(),
            "total_job_scan_output":[out.model_dump()], 
            "count_scraped_posts":post_count+1,
            "job_count": 0
        }
    return {}




#forth Node:
def find_relevant_jobs(state):
    raw_scan = state.get("job_scan_output")
    if not raw_scan:
        return {"relevant_jobs": [], "irrelevant": [], "post_relevant_count": 0}
    scan = PostExtraction.model_validate(raw_scan)

    jobs = scan.jobs
    relevant_jobs = []
    irrelevant = []

    if not scan.is_hiring_post:
        return {"relevant_jobs": [], "irrelevant": [], "post_relevant_count": 0}

    for job in jobs:
        reason = []
        if not job.is_role_relevant: 
            reason.append("Role not relevant")
          
        if not job.location_in_india_or_unspecified:
            reason.append(f"Outside India: {job.location}")
          
        if job.min_experience_years is not None and job.min_experience_years >= 4:
            reason.append(f"Requires {job.min_experience_years}+ yrs")

        if reason:
            irrelevant.append({
                "company":job.company,
                "reason": " | ".join(reason),
                "role":job.role,
                "application_requirements":job.application_requirements,
                "location":job.location,
                "min_experience_years":job.min_experience_years
            })
            continue

        email = (job.contact_email or "").lower()
        apply_link = job.apply_link or ""
        whatsapp_or_phone = job.whatsapp_or_phone or ""
        relevant_jobs.append({
            "is_positive_email" : True if email else False,
            "contact_email": job.contact_email if email else None,
            "is_whatsapp_contact" : True if whatsapp_or_phone else False,
            "whatsapp_or_phone":job.whatsapp_or_phone if whatsapp_or_phone else None,
            "is_link" : True if apply_link else False,
            "apply_link": job.apply_link if apply_link else None,
            "is_dm_on_linkedin":job.is_dm_on_linkedin,
            "company":job.company,
            "role":job.role,
            "application_requirements":job.application_requirements,
            "location":job.location,
            "min_experience_years":job.min_experience_years,
            "apply_methods":[k for k,v in {"email":email, "link":apply_link, "whatsapp":whatsapp_or_phone}.items() if v],
        })
    return {
        "relevant_jobs":relevant_jobs,
        "irrelevant":irrelevant, 
        "total_relevant_jobs":relevant_jobs,
        "total_irrelevant":irrelevant,
        "post_relevant_count":len(relevant_jobs)
    }



#fifth Node:
def email_draft(state):
    jobs = state.get("relevant_jobs", [])
    job = jobs[state.get("job_count", 0)]

    values = {
        **CANDIDATE,
        "company": job.get("company") or "your company",
        "role": job.get("role") or "AI Engineer",
    }
    return {
        "email_subject": EMAIL_SUBJECT.format(**values),
        "email_body": EMAIL_FORMAT.format(**values),
    }



#Sixth Node:
def build_message(to, subject, body, attachment_path=None):
    msg = EmailMessage()
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    if attachment_path:
        ctype, _ = mimetypes.guess_type(attachment_path)
        maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
        with open(attachment_path, "rb") as f:
            msg.add_attachment(f.read(), maintype=maintype, subtype=subtype,
                               filename=os.path.basename(attachment_path))
    return {"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}

def load_sent_emails():
    if os.path.exists(settings.SENT_FILE):
        with open(settings.SENT_FILE) as f:
            return json.load(f)
    return []

def save_sent_email(addr):
    sent = load_sent_emails()
    if addr not in sent:
        sent.append(addr)
        with open(settings.SENT_FILE, "w") as f:
            json.dump(sent, f, indent=2)

def email_send(state):
    job_count = state.get("job_count", 0)
    job = state["relevant_jobs"][job_count]
    to = (job.get("contact_email") or "").strip().lower()

    if not to or to in state.get("unique_email", []):
        return {"job_count": job_count + 1}

    try:
        if settings.DRY_RUN:
            print(f"[DRY RUN] To: {to}\nSubject: {state['email_subject']}\n\n{state['email_body']}\n")
        else:
            service = get_gmail_service()
            message = build_message(to, state["email_subject"], state["email_body"], settings.RESUME_PATH)
            service.users().messages().send(userId="me", body=message).execute()
    except Exception as e:
        print(f"[FAILED] {to}: {e}")
        return {"job_count": job_count + 1}

    if not settings.DRY_RUN:
        try:
            save_sent_email(to)
        except Exception as e:
            print(f"[WARN] Sent to {to} but could not save it to {settings.SENT_FILE}: {e}")

    return {"job_count": job_count + 1, "unique_email": [to]}



#seventh Node:
def others(state):
    """ In futer for router for whatsapp, link, or DM msgs"""
    job_count = state.get("job_count",0)

    return{"job_count": job_count+1}