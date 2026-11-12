from __future__ import annotations
from config import settings

__all__ = [
    "CANDIDATE",
    "EMAIL_FORMAT",
    "EMAIL_SUBJECT",
]

CANDIDATE = {
    "name": settings.NAME,
    "phone": settings.PHONE,
    "email": settings.EMAIL,
    "linkedin": settings.LINKEDIN,
}

EMAIL_SUBJECT = "Application for {role} Position - {name}"

EMAIL_FORMAT = """Dear Hiring Team at {company},

I am writing to express my strong interest in the {role} position at {company}.

As an AI Engineer with a Master's degree in Mathematics and Computing from NIT Allahabad (MNNIT) and over a year of hands-on experience building production-grade Generative AI systems, RAG pipelines, and agentic workflows, I am eager to contribute to your team.

Here is a brief overview of how my technical background aligns with your requirements:
- Generative AI & LLMs: Extensive experience working with OpenAI API, Anthropic Claude, and Amazon Bedrock, along with prompt engineering and function/tool-calling implementations.
- RAG & Retrieval: Production experience building end-to-end RAG pipelines, semantic search engines, and hybrid retrieval systems using pgvector and ChromaDB.
- Agentic Frameworks & Backend: Strong proficiency in building autonomous multi-agent workflows using LangGraph and CrewAI, backed by scalable FastAPI backends containerized with Docker on AWS.
- Core Technical Stack: Python (Expert), SQL, PyTorch, scikit-learn, and evaluation frameworks like LangSmith and ragas.

I have attached my resume for your review and would welcome the opportunity to discuss how my background matches the goals of {company}.

Best regards,

{name}
{phone} | {email} | LinkedIn: {linkedin}"""
