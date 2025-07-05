from fastapi import APIRouter

router = APIRouter()

@router.get("/sample")
def read_sample() -> dict:
    """Read sample data.

    Call this endpoint to retrieve a sample message.

    Returns:
        dict: A dictionary containing the sample message.
    """
    return {"message": "Sample endpoint"}
