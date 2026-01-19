from pydantic import BaseModel
from typing import Optional, Dict, Any

class CommandAPIResponse(BaseModel):
    status: str
    action: str
    text: str
    intent: Optional[Dict[str, Any]] = None
