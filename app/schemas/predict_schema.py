from pydantic import BaseModel, AnyHttpUrl
from typing import Optional

class URLRequest(BaseModel):
    url: str

class PredictionResponse(BaseModel):
    status: str
    prediction: str
    reasons: Optional[list] = None
    message: Optional[str] = None
