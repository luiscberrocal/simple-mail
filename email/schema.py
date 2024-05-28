from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field

from .enums import EmailFormat


class SenderConfig(BaseModel):
    email: str
    password: str


class EmailMessage(BaseModel):
    recipients: List[str] = Field(description="Recipients")
    subject: str = Field(description="Subject")
    content: str = Field(description="Content")
    sender_config: SenderConfig = Field(description="Sender configuration")
    attachments: Optional[List[Path] | None]
    format: EmailFormat = Field(default=EmailFormat.TEXT)
