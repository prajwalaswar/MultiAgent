from pydantic import BaseModel, Field
from typing import List


class ChatRequest(BaseModel):
    model_name: str = Field(..., description="Model identifier")
    model_provider: str = Field(..., description="Provider name: Groq or OpenAI")
    system_prompt: str = Field("Act as an AI chatbot who is smart and friendly")
    messages: List[str]
    allow_search: bool = False


class ChatResponse(BaseModel):
    response: str
