import uvicorn

from vibra.utils import Settings

from .app import app


def run_api() -> None:  # pragma: no cover
    uvicorn.run(app, host="0.0.0.0", port=Settings.APPLICATION_PORT)


__all__ = ["run_api"]
