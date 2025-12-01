from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal

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
    Localized,
    PodcastStatus,
    PrivacyStatus,
    Thumbnails,
    validate_id,
    validate_part,
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

    @field_validator("part", mode="before")
    def validate_part(cls, v: Any):
        return validate_part(v, PlaylistPart)

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
    channel_id: str | None = Field(
        None,
        alias="channelId",
        description="YouTube channel ID",
    )

    id: list[str] | None = Field(
        None,
        description="List of YouTube playlist IDs or comma-separated string",
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

    mine: bool | None = Field(
        None,
        description="Return only playlists owned by authenticated user",
    )

    @model_validator(mode="after")
    def validate_exactly_one_filter(self):
        filter_fields = ["channel_id", "id", "mine"]
        specified = [f for f in filter_fields if getattr(self, f) is not None]

        if len(specified) != 1:
            raise ValueError(
                "Exactly one filter must be specified: "
                "channelId, id, mine. "
                f"Got: {specified or 'none'}"
            )

        return self

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
