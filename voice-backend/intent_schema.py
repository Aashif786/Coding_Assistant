from pydantic import BaseModel
from typing import Optional

class IntentResult(BaseModel):
    intent: str
    language: Optional[str] = None
    name: Optional[str] = None
    line: Optional[int] = None
