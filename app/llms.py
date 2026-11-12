from __future__ import annotations
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

from app.schemas import PostExtraction
from config import settings


llm_decision = ChatGoogleGenerativeAI(
    model=settings.GEMINI_DECISION_MODEL,
    temperature=0,
    google_api_key=settings.GEMINI_API_KEY,
)

llm_decision_job_extraction = llm_decision.with_structured_output(PostExtraction)
