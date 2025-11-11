from pydantic import BaseModel
from typing import Optional

# Example schema
class ExampleResponse(BaseModel):
    message: str
    status: Optional[str] = "success"

