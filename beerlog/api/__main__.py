"""Beerlog API main script."""

# Scripts that manipulate the shell must always be careful with possible
# security implications.
import subprocess  # nosec

from fastapi import APIRouter, FastAPI

from beerlog.api.routes import beers
from beerlog.config import settings

api = FastAPI(
    title="Beerlog",
    description="List of all service's endpoints.",
    docs_url="/",
)

api_router = APIRouter()

api_router.include_router(beers.router)

api.include_router(api_router)


def main() -> None:
    """Start Beerlog API."""
    command = (
        "uvicorn beerlog.api.__main__:api "  # nosec
        f"--host={settings.get('API_HOST', default='0.0.0.0')} "
        f"--port={settings.get('API_PORT', default=8000)} "
        "--reload"
    )
    try:
        subprocess.run(
            command, shell=True, check=True, encoding="utf-8"  # nosec
        )
    except KeyboardInterrupt:
        pass  # User stopped the service
