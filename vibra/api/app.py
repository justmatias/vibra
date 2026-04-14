from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from vibra.api.routers import auth_router
from vibra.utils import Settings

app = FastAPI(title="Vibra API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")
