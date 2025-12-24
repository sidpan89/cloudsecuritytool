from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes import router
from backend.app.core.config import get_settings
from backend.app.db.session import Base, engine

settings = get_settings()

app = FastAPI(title='Aura Guard Backend')

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router)


@app.on_event('startup')
def startup():
    """Ensure database tables exist for local dev/test environments."""
    Base.metadata.create_all(bind=engine)
