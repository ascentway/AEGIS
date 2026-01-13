from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
from app.core.config import settings
from app.core.database import db
from app.routes import auth, players, organizations

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    print(f"\n[INCOMING] {request.method} {request.url}")
    try:
        print(f"[PARAMS] {request.query_params}")
    except Exception:
        pass

    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    print(f"[OUTGOING] Status: {response.status_code} | Time: {process_time:.2f}ms")
    return response

# Database events
@app.on_event("startup")
async def startup_db_client():
    db.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    db.close()

# Routes
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(players.router, prefix=f"{settings.API_V1_STR}/players", tags=["players"])
app.include_router(organizations.router, prefix=f"{settings.API_V1_STR}/organizations", tags=["organizations"])

@app.get("/")
async def root():
    return {"message": "Welcome to Esports Scouting Platform API"}
