from enum import Enum
from typing import Any, List, Type

from pydantic import BaseModel, Field


class PrivacyStatus(str, Enum):
    """Privacy status of the channel."""

    PRIVATE = "private"
    PUBLIC = "public"
    UNLISTED = "unlisted"


class LongUploadsStatus(str, Enum):
    """Long uploads eligibility status."""

    ALLOWED = "allowed"
    DISALLOWED = "disallowed"
    ELIGIBLE = "eligible"


class ThumbnailSize(str, Enum):
    """Thumbnail image size options."""

    DEFAULT = "default"
    MEDIUM = "medium"
    HIGH = "high"


class PodcastStatus(str, Enum):
    """Podcast status of the playlist."""

    ENABLED = "enabled"
    DISABLED = "disabled"
    UNSPECIFIED = "unspecified"


class Thumbnail(BaseModel):
    """Represents a thumbnail image."""

    url: str
    width: int | None = None
    height: int | None = None


class Thumbnails(BaseModel):
    """Collection of thumbnail images in different sizes."""

    default: Thumbnail | None = None
    medium: Thumbnail | None = None
    high: Thumbnail | None = None


class Localized(BaseModel):
    """Localized title and description."""

    title: str
    description: str


class ListRequestMixin:
    """Mixin for paginated list requests."""

    page_token: str | None = Field(
        None, alias="pageToken", description="Token for specific page in result set"
    )


class ListResponseMixin:
    """Mixin for paginated list responses."""

    etag: str | None = None
    next_page_token: str | None = Field(None, alias="nextPageToken")
    prev_page_token: str | None = Field(None, alias="prevPageToken")
    page_info: dict[str, int] | None = Field(None, alias="pageInfo")


def validate_part(v: Any, enum: Type[Enum]) -> List[str]:
    """Generic validator for part parameters - accepts string or list and validates against enum."""
    valid_parts = {part.value for part in enum}

    # Handle both string and list inputs
    if isinstance(v, str):
        parts = [p.strip() for p in v.split(",")]
    elif isinstance(v, list):
        parts = []
        for p in v:
            if hasattr(p, "value"):  # Handle enum values
                parts.append(p.value)
            else:
                parts.append(str(p).strip())
    else:
        raise ValueError("Part must be a string or list of strings")

    # Validate all parts are valid
    invalid_parts = [p for p in parts if p not in valid_parts]
    if invalid_parts:
        raise ValueError(
            f"Invalid part(s): {', '.join(invalid_parts)}. Valid parts: {', '.join(sorted(valid_parts))}"
        )

    return parts


def validate_id(v: Any) -> List[str] | None:
    """Generic validator for ID list parameters - accepts string or list."""
    if v is None:
        return v

    # Handle both string and list inputs
    if isinstance(v, str):
        ids = [id_val.strip() for id_val in v.split(",") if id_val.strip()]
    elif isinstance(v, list):
        ids = [str(id_val).strip() for id_val in v if str(id_val).strip()]
    else:
        raise ValueError("ID must be a string or list of strings")

    if not ids:
        raise ValueError("At least one ID must be provided")

    return ids
