from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field

from .enums import EmailFormat


class SenderConfig(BaseModel):
    """Sender configuration. Information about the sender."""
    email: str = Field(description="Email address of the sender")
    password: str = Field(description="Password of the sender. Acually it is an app password.")


class EmailMessage(BaseModel):
    """Email message. Information about the email message."""
    recipients: List[str] = Field(description="Recipients")
    subject: str = Field(description="Subject")
    content: str = Field(description="Content")
    sender_config: SenderConfig = Field(description="Sender configuration")
    attachments: Optional[List[Path] | None] = Field(description="Attachments", default=None)
    format: EmailFormat = Field(default=EmailFormat.TEXT)
