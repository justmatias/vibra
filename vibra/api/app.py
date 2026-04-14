from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(title="Vibra API")


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")
