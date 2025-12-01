from datetime import datetime
from enum import Enum
from typing import Any, List, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    FieldSerializationInfo,
    field_serializer,
    field_validator,
    model_validator,
)

from .model import (
    ListRequestMixin,
    ListResponseMixin,
    PrivacyStatus,
    Thumbnails,
    validate_id,
    validate_part,
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

    @field_validator("part", mode="before")
    def validate_part(cls, v: Any):
        return validate_part(v, PlaylistItemPart)

    @field_serializer("part")
    def serialize_part(
        self,
        v: list[str],
        info: FieldSerializationInfo,
    ) -> str | list[str]:
        if info.context and info.context.get("comma_separated"):
            return ",".join(v)

        return v

    # Filter parameters (exactly one must be specified)
    id: list[str] | None = Field(
        None,
        description="List of playlist item IDs or comma-separated string",
    )

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: Any):
        return validate_id(v)

    @field_serializer("id")
    def serialize_id(
        self,
        v: list[str] | None,
        info: FieldSerializationInfo,
    ) -> str | list[str] | None:
        if v is None:
            return v

        if info.context and info.context.get("comma_separated"):
            return ",".join(v)

        return v

    playlist_id: str | None = Field(
        None,
        alias="playlistId",
        description="ID of the playlist for which to retrieve playlist items",
    )

    @model_validator(mode="after")
    def validate_exactly_one_filter(self):
        filter_fields = ["id", "playlist_id"]
        specified = [f for f in filter_fields if getattr(self, f) is not None]

        if len(specified) != 1:
            raise ValueError(
                "Exactly one filter must be specified: "
                "id, playlistId. "
                f"Got: {specified or 'none'}"
            )

        return self

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
