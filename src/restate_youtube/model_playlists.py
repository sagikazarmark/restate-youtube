from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from .model import (
    ListRequestMixin,
    ListResponseMixin,
    Localized,
    PodcastStatus,
    PrivacyStatus,
    Thumbnails,
)


class PlaylistPart(str, Enum):
    """Playlist resource parts that can be included in API responses."""

    CONTENT_DETAILS = "contentDetails"
    ID = "id"
    LOCALIZATIONS = "localizations"
    PLAYER = "player"
    SNIPPET = "snippet"
    STATUS = "status"


class PlaylistSnippet(BaseModel):
    """Basic details about the playlist."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    published_at: datetime | None = Field(default=None, alias="publishedAt")
    channel_id: str | None = Field(None, alias="channelId")
    title: str
    description: str
    thumbnails: Thumbnails | None = None
    channel_title: str | None = Field(None, alias="channelTitle")
    default_language: str | None = Field(None, alias="defaultLanguage")
    localized: Localized | None = None


class PlaylistStatus(BaseModel):
    """Privacy status and other playlist settings."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    privacy_status: PrivacyStatus | None = Field(None, alias="privacyStatus")
    podcast_status: PodcastStatus | None = Field(None, alias="podcastStatus")


class PlaylistContentDetails(BaseModel):
    """Information about the playlist's content."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    item_count: int | None = Field(None, alias="itemCount")


class PlaylistPlayer(BaseModel):
    """Information for playing the playlist in an embedded player."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    embed_html: str | None = Field(None, alias="embedHtml")


class Playlist(BaseModel):
    """A YouTube playlist resource."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    kind: Literal["youtube#playlist"] = Field(default="youtube#playlist")
    etag: str | None = None
    id: str | None = None
    snippet: PlaylistSnippet | None = None
    status: PlaylistStatus | None = None
    content_details: PlaylistContentDetails | None = Field(None, alias="contentDetails")
    player: PlaylistPlayer | None = None
    localizations: Dict[str, Localized] | None = None


class ListAllPlaylistsRequest(BaseModel):
    """Request parameters for the YouTube Data API playlists.list endpoint."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    part: list[PlaylistPart] = Field(
        description="List of playlist resource properties to include in the response",
    )

    # Internal configuration for serialization behavior
    _serialize_part_as_string: bool = False

    # Filter parameters (exactly one must be specified)
    channel_id: str | None = Field(
        None, alias="channelId", description="YouTube channel ID"
    )
    id: str | None = Field(
        None, description="Comma-separated list of YouTube playlist IDs"
    )
    mine: bool | None = Field(
        None, description="Return only playlists owned by authenticated user"
    )

    # Optional parameters
    hl: str | None = Field(None, description="Language code for localized metadata")
    on_behalf_of_content_owner: str | None = Field(
        None,
        alias="onBehalfOfContentOwner",
        description="Content owner on whose behalf the request is made",
    )
    on_behalf_of_content_owner_channel: str | None = Field(
        None,
        alias="onBehalfOfContentOwnerChannel",
        description="YouTube channel ID of the channel to which a video is being added",
    )

    @field_validator("part", mode="before")
    @classmethod
    def validate_part(cls, v):
        """Parse and validate part parameter - accepts string or list."""
        valid_parts = {part.value for part in PlaylistPart}

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

    @field_serializer("part")
    def serialize_part(self, v: list[str]) -> str | list[str]:
        """Serialize part list to comma-separated string or keep as list based on configuration."""
        if self._serialize_part_as_string:
            return ",".join(v)
        return v

    def __init__(self, **data):
        super().__init__(**data)
        # Validate that exactly one filter parameter is specified
        filter_params = [
            self.channel_id,
            self.id,
            self.mine,
        ]
        specified_filters = [p for p in filter_params if p is not None]

        if len(specified_filters) != 1:
            raise ValueError(
                "Exactly one filter parameter must be specified: channelId, id, or mine"
            )

    def model_dump(
        self,
        *,
        serialize_part_as_string: bool = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        # Temporarily set the serialization behavior
        original_value = self._serialize_part_as_string
        self._serialize_part_as_string = serialize_part_as_string

        try:
            return super().model_dump(**kwargs)
        finally:
            # Restore original value
            self._serialize_part_as_string = original_value

    def model_dump_for_api(self, **kwargs: Any) -> Dict[str, Any]:
        return self.model_dump(serialize_part_as_string=True, **kwargs)

    def model_dump_for_schema(self, **kwargs: Any) -> Dict[str, Any]:
        return self.model_dump(serialize_part_as_string=False, **kwargs)


class ListAllPlaylistsResponse(BaseModel):
    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    kind: Literal["youtube#playlistListResponse"] = Field(
        default="youtube#playlistListResponse"
    )
    items: List[Playlist] = Field(default_factory=list)


class ListPlaylistsRequest(ListAllPlaylistsRequest, ListRequestMixin):
    max_results: int | None = Field(
        None,
        alias="maxResults",
        ge=0,
        le=50,
        description="Maximum number of results (0-50, default 5)",
    )


class ListPlaylistsResponse(ListAllPlaylistsResponse, ListResponseMixin):
    pass
