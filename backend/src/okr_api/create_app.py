import typing as t
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Call this to initialize the FastAPI app with routers.

    Returns:
        FastAPI: The initialized FastAPI application.
    """
    app = FastAPI()

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8501"],  # Frontend origin
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Import and include routers here
    from .endpoints.sample import router as sample_router
    app.include_router(sample_router)
    from .endpoints.objectives import router as objectives_router
    app.include_router(objectives_router)
    from .endpoints.key_results import router as key_results_router
    app.include_router(key_results_router)

    return app
