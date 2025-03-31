from pydantic import BaseModel
from typing import Optional


class UrlCreateSchema(BaseModel):
    url: str
    custom_alias: Optional[str]
    expires_at: Optional[str]


class UrlUpdateSchema(BaseModel):
    new_short_code: str
    expires_at: Optional[str]
