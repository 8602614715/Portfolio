import re
import unicodedata
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints, field_validator

NAME_MIN, NAME_MAX = 2, 100
MESSAGE_MIN, MESSAGE_MAX = 5, 2000

_NAME_SEPARATORS = " .'’-"


def _is_valid_name(value: str) -> bool:
    """Letters/combining marks of any script, with single separators between them."""
    if not unicodedata.category(value[0]).startswith("L"):
        return False
    previous_was_separator = False
    for char in value:
        is_separator = char in _NAME_SEPARATORS
        if is_separator and previous_was_separator and char != " ":
            return False
        if not is_separator and unicodedata.category(char)[0] not in ("L", "M"):
            return False
        previous_was_separator = is_separator
    return True


def _contains_control_chars(value: str, allow: str = "") -> bool:
    return any(unicodedata.category(c) == "Cc" and c not in allow for c in value)


class ContactRequest(BaseModel):
    """Public contact form payload. Whitespace is trimmed before length checks."""

    model_config = ConfigDict(extra="forbid")

    name: Annotated[str, StringConstraints(strip_whitespace=True)] = Field(
        min_length=NAME_MIN, max_length=NAME_MAX, examples=["Ada Lovelace"]
    )
    email: EmailStr = Field(max_length=254, examples=["ada@example.com"])
    message: Annotated[str, StringConstraints(strip_whitespace=True)] = Field(
        min_length=MESSAGE_MIN,
        max_length=MESSAGE_MAX,
        examples=["Hi Satyam, I'd love to talk about a project."],
    )

    @field_validator("name")
    @classmethod
    def _validate_name(cls, value: str) -> str:
        value = re.sub(r"\s+", " ", value)
        if not _is_valid_name(value):
            raise ValueError("Name may only contain letters, spaces, hyphens, apostrophes and periods")
        return value

    @field_validator("email")
    @classmethod
    def _normalise_email(cls, value: str) -> str:
        return value.lower()

    @field_validator("message")
    @classmethod
    def _validate_message(cls, value: str) -> str:
        # Allow newlines and tabs; reject NUL and other control characters.
        if _contains_control_chars(value, allow="\n\r\t"):
            raise ValueError("Message contains invalid control characters")
        return value


class ContactResponse(BaseModel):
    success: bool = True
    message: str = "Thanks for reaching out! Your message has been received."
