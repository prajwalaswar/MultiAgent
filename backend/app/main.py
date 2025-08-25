import uvicorn
from fastapi import FastAPI
import os, sys
from dotenv import load_dotenv
load_dotenv()

# Support both package-run and script-run
try:
    from .core.config import get_settings
    from .core.logging_config import setup_logging
    from .api.routes import router as api_router
except Exception:
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from app.core.config import get_settings
    from app.core.logging_config import setup_logging
    from app.api.routes import router as api_router


def create_app() -> FastAPI:
    setup_logging()
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.version)

    app.include_router(api_router)

    @app.get("/")
    def root():
        return {"message": f"{settings.app_name} is running"}

    return app


app = create_app()


if __name__ == "__main__":
    s = get_settings()
    # Run directly with the app object to avoid module path issues when executed as a script
    uvicorn.run(app, host=s.host, port=s.port, reload=False)
