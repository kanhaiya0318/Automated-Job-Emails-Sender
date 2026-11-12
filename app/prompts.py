from langchain_core.prompts import ChatPromptTemplate

from app.llms import llm_decision_job_extraction

extraction_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You extract job openings from a LinkedIn post.\n"
     "Rules:\n"
     "- is_hiring_post is True only when an employer or recruiter is hiring. "
     "False for job seekers, ads, courses/bootcamps and general posts.\n"
     "- Create one JobListing per distinct job. Do not merge jobs.\n"
     "- Match contact details to the job they appear under. If an email, phone "
     "or link is not clearly tied to that job, leave it None. Never guess.\n"
     "- Copy emails exactly, without the 'mailto:' prefix.\n"
     "- apply_link must be a real application, job-page or form URL. "
     "Ignore hashtags, bootcamp, course and promo links.\n"
     "- is_role_relevant is True only for full-time or internship roles in "
     "AI/ML/GenAI/LLM or Python backend. False for data analyst, data "
     "governance, sales, ERP/HCM, testing and similar.\n"
     "- location_in_india_or_unspecified is True if the job is in India, "
     "remote, or has no location. False only if it is restricted to another country.\n"
     "- If a value is not stated in the post, use None."),
    ("human",
     "Post content:\n{content}\n\n"
     "Links and emails found in the post:\n{links}\n\n"
     "Post URL: {post_url}"),
])

job_extraction_chain = extraction_prompt | llm_decision_job_extraction