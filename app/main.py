from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer  # security scheme
from fastapi_mcp import FastApiMCP
from app.config.db_config import init_db
from app.routers import agent, chatbot, predict, mcp, chat_services, project_routes, ticket_agentic_services, unit_routes
from .logger import logger
from .middleware import Middleware
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from fastapi.middleware.cors import CORSMiddleware
import app.model
from app.workflow.ticket_trans_graph import ticket_trans_workflow
from IPython.display import Image, display
import io

load_dotenv()

security = HTTPBearer()

API_TOKEN = os.getenv("API_TOKEN")

@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="AI Agentic API",
    description="AI Agentic API designed for you guys",
    version="1.0.0",
    lifespan=lifespan
)

routes = [
    agent.router,
    predict.router,
    chatbot.router,
    chat_services.router,
    project_routes.router,
    unit_routes.router,
    ticket_agentic_services.router
]

for i in routes:
    app.include_router(i)

app.add_middleware(Middleware)

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=os.getenv("DB_URL"),
)

app.add_middleware(
    CORSMiddleware,
        allow_origins=['http://localhost:6500',
        "http://localhost",
        "http://localhost:61497",
        "http://localhost:8000",
        '*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
)
# Create an MCP server based on this app
mcp = FastApiMCP(
    app,
    include_operations=["get_csv_data"]
)

# Mount the MCP server directly to your app
mcp.mount()

# Dependency to verify Bearer Token
def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials.credentials

@app.get("/")
async def root():
    logger.info('Request to index page')
    return StreamingResponse(
        io.BytesIO(ticket_trans_workflow.get_graph().draw_mermaid_png()),
        media_type="image/png",
        headers={"Content-Disposition": "inline; filename=workflow.png"}
    )
    # return {"message": "Hello World!", "description": app.description}