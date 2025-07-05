import uvicorn
from .create_app import create_app


def run_server():
    """Run the Uvicorn server.

    Call this to start the FastAPI application using Uvicorn.
    """
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_server()
