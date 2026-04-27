from pydantic import BaseModel
from typing import Optional, Dict, Any

class CommandAPIResponse(BaseModel):
    status: str
    action: str
    text: str
    line: Optional[int] = None
    line_end: Optional[int] = None
    intent: Optional[Dict[str, Any]] = None