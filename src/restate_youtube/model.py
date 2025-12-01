from enum import Enum

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
