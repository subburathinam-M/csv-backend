from pydantic import BaseModel


class ProcessResponse(BaseModel):
    message: str
    total_rows: int
    duplicate_rows: int
    unique_rows: int
