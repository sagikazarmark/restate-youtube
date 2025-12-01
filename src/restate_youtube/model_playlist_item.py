from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from .model import (
    ListRequestMixin,
    ListResponseMixin,
    PrivacyStatus,
    Thumbnails,
)


class PlaylistItemPart(str, Enum):
    """Playlist item resource parts that can be included in API responses."""

    CONTENT_DETAILS = "contentDetails"
    ID = "id"
    SNIPPET = "snippet"
    STATUS = "status"


class ResourceId(BaseModel):
    """Resource identification for playlist items."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    kind: str | None = None
    video_id: str | None = Field(None, alias="videoId")


class PlaylistItemSnippet(BaseModel):
    """Snippet information for a playlist item."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    published_at: datetime | None = Field(None, alias="publishedAt")
    channel_id: str | None = Field(None, alias="channelId")
    title: str | None = None
    description: str | None = None
    thumbnails: Thumbnails | None = None
    channel_title: str | None = Field(None, alias="channelTitle")
    playlist_id: str | None = Field(None, alias="playlistId")
    position: int | None = None
    resource_id: ResourceId | None = Field(None, alias="resourceId")
    video_owner_channel_title: str | None = Field(None, alias="videoOwnerChannelTitle")
    video_owner_channel_id: str | None = Field(None, alias="videoOwnerChannelId")


class PlaylistItemContentDetails(BaseModel):
    """Content details for a playlist item."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    video_id: str | None = Field(None, alias="videoId")
    start_at: str | None = Field(None, alias="startAt")
    end_at: str | None = Field(None, alias="endAt")
    note: str | None = None
    video_published_at: datetime | None = Field(None, alias="videoPublishedAt")


class PlaylistItemStatus(BaseModel):
    """Status information for a playlist item."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    privacy_status: PrivacyStatus | None = Field(None, alias="privacyStatus")


class PlaylistItem(BaseModel):
    """A YouTube playlist item resource."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    kind: Literal["youtube#playlistItem"] = Field(default="youtube#playlistItem")
    etag: str | None = None
    id: str | None = None
    snippet: PlaylistItemSnippet | None = None
    content_details: PlaylistItemContentDetails | None = Field(
        None, alias="contentDetails"
    )
    status: PlaylistItemStatus | None = None


class ListAllPlaylistItemsRequest(BaseModel):
    """Request parameters for listing all playlist items from the YouTube Data API playlistItems.list endpoint."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    part: list[PlaylistItemPart] = Field(
        description="List of playlist item resource properties to include in the response",
    )

    # Internal configuration for serialization behavior
    _serialize_part_as_string: bool = False

    # Filter parameters (exactly one must be specified)
    id: str | None = Field(
        None,
        description="Comma-separated list of playlist item IDs",
    )
    playlist_id: str | None = Field(
        None,
        alias="playlistId",
        description="ID of the playlist for which to retrieve playlist items",
    )

    # Optional parameters
    video_id: str | None = Field(
        None,
        alias="videoId",
        description="Return only playlist items that contain the specified video",
    )
    on_behalf_of_content_owner: str | None = Field(
        None,
        alias="onBehalfOfContentOwner",
        description="YouTube CMS user acting on behalf of content owner",
    )

    @field_validator("part", mode="before")
    def validate_part(cls, v):
        """Validate and convert part parameter to list of PlaylistItemPart enums."""
        if isinstance(v, str):
            parts = [part.strip() for part in v.split(",")]
        elif isinstance(v, list):
            parts = v
        else:
            raise ValueError("part must be a string or list")

        validated_parts = []
        for part in parts:
            try:
                validated_parts.append(PlaylistItemPart(part))
            except ValueError:
                raise ValueError(
                    f"Invalid part '{part}'. Must be one of: {[p.value for p in PlaylistItemPart]}"
                )
        return validated_parts

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
            self.id,
            self.playlist_id,
        ]
        specified_filters = [p for p in filter_params if p is not None]

        if len(specified_filters) != 1:
            raise ValueError(
                "Exactly one filter parameter must be specified: id or playlistId"
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


class ListAllPlaylistItemsResponse(BaseModel):
    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    kind: Literal["youtube#playlistItemListResponse"] = Field(
        default="youtube#playlistItemListResponse"
    )
    items: List[PlaylistItem] = Field(default_factory=list)


class ListPlaylistItemsRequest(ListAllPlaylistItemsRequest, ListRequestMixin):
    max_results: int | None = Field(
        None,
        alias="maxResults",
        ge=0,
        le=50,
        description="Maximum number of results (0-50, default 5)",
    )


class ListPlaylistItemsResponse(ListAllPlaylistItemsResponse, ListResponseMixin):
    pass
