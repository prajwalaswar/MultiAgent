Backend structure

backend/
  app/
    api/
      routes.py
    core/
      config.py
      logging_config.py
    schemas/
      chat.py
    services/
      agent_service.py
    main.py

Run locally:
- cd Agent/ai-agent-chatbot-with-fastapi/backend
- python -m uvicorn app.main:app --host 127.0.0.1 --port 9999 --reload

Endpoints:
- GET  /           -> root message
- GET  /api/health -> health check
- GET  /api/models -> available models (optional ?provider=Groq|OpenAI)
- GET  /api/info   -> app info
- POST /api/chat   -> chat with the agent
