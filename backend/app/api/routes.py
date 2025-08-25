from fastapi import APIRouter, HTTPException
from ..schemas.chat import ChatRequest, ChatResponse
from ..core.config import get_settings
from ..services.agent_service import run_agent

router = APIRouter(prefix="/api", tags=["api"]) 


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/models")
def list_models(provider: str | None = None):
    settings = get_settings()
    if provider:
        return {provider: settings.models_by_provider.get(provider, [])}
    return settings.models_by_provider


@router.get("/info")
def info():
    s = get_settings()
    return {"app": s.app_name, "version": s.version, "env": s.environment}


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    settings = get_settings()
    allowed = settings.models_by_provider.get(req.model_provider, [])
    if req.model_name not in allowed:
        raise HTTPException(status_code=400, detail="Invalid model name for provider")

    # Fail fast if required keys are missing
    if req.model_provider == "Groq" and not settings.groq_api_key:
        raise HTTPException(status_code=500, detail="Missing GROQ_API_KEY in .env")
    if req.model_provider == "OpenAI" and not settings.openai_api_key:
        raise HTTPException(status_code=500, detail="Missing OPENAI_API_KEY in .env")

    try:
        result = run_agent(
            provider=req.model_provider,
            model_name=req.model_name,
            messages=req.messages,
            allow_search=req.allow_search,
            system_prompt=req.system_prompt,
        )
        return ChatResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
