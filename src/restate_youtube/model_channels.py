from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from .model import (
    ListRequestMixin,
    ListResponseMixin,
    Localized,
    LongUploadsStatus,
    PrivacyStatus,
    Thumbnails,
    validate_id,
    validate_part,
)


class ChannelPart(str, Enum):
    """Channel resource parts that can be included in API responses."""

    AUDIT_DETAILS = "auditDetails"
    BRANDING_SETTINGS = "brandingSettings"
    CONTENT_DETAILS = "contentDetails"
    CONTENT_OWNER_DETAILS = "contentOwnerDetails"
    ID = "id"
    LOCALIZATIONS = "localizations"
    SNIPPET = "snippet"
    STATISTICS = "statistics"
    STATUS = "status"
    TOPIC_DETAILS = "topicDetails"


class ChannelSnippet(BaseModel):
    """Basic details about the channel."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    title: str
    description: str
    custom_url: str | None = Field(None, alias="customUrl")
    published_at: datetime | None = Field(default=None, alias="publishedAt")
    thumbnails: Thumbnails | None = None
    default_language: str | None = Field(None, alias="defaultLanguage")
    localized: Localized | None = None
    country: str | None = None


class RelatedPlaylists(BaseModel):
    """Playlists associated with the channel."""

    likes: str | None = None
    uploads: str | None = None


class ContentDetails(BaseModel):
    """Information about the channel's content."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    related_playlists: RelatedPlaylists | None = Field(None, alias="relatedPlaylists")


class Statistics(BaseModel):
    """Statistics for the channel."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    view_count: int | None = Field(None, alias="viewCount")
    subscriber_count: int | None = Field(None, alias="subscriberCount")
    hidden_subscriber_count: bool | None = Field(None, alias="hiddenSubscriberCount")
    video_count: int | None = Field(None, alias="videoCount")


class TopicDetails(BaseModel):
    """Topics associated with the channel."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    topic_categories: List[str] | None = Field(None, alias="topicCategories")


class Status(BaseModel):
    """Privacy status and other channel settings."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    privacy_status: PrivacyStatus | None = Field(None, alias="privacyStatus")
    is_linked: bool | None = Field(None, alias="isLinked")
    long_uploads_status: LongUploadsStatus | None = Field(
        None, alias="longUploadsStatus"
    )
    made_for_kids: bool | None = Field(None, alias="madeForKids")
    self_declared_made_for_kids: bool | None = Field(
        None, alias="selfDeclaredMadeForKids"
    )


class BrandingChannel(BaseModel):
    """Branding properties of the channel page."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    title: str | None = None
    description: str | None = None
    keywords: str | None = None
    tracking_analytics_account_id: str | None = Field(
        None, alias="trackingAnalyticsAccountId"
    )
    unsubscribed_trailer: str | None = Field(None, alias="unsubscribedTrailer")
    default_language: str | None = Field(None, alias="defaultLanguage")
    country: str | None = None


class BrandingSettings(BaseModel):
    """Branding settings for the channel."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    channel: BrandingChannel | None = None


class AuditDetails(BaseModel):
    """Channel audit information for multichannel networks."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    overall_good_standing: bool | None = Field(None, alias="overallGoodStanding")
    community_guidelines_good_standing: bool | None = Field(
        None, alias="communityGuidelinesGoodStanding"
    )
    copyright_strikes_good_standing: bool | None = Field(
        None, alias="copyrightStrikesGoodStanding"
    )
    content_id_claims_good_standing: bool | None = Field(
        None, alias="contentIdClaimsGoodStanding"
    )


class ContentOwnerDetails(BaseModel):
    """Content owner details visible only to YouTube Partners."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    content_owner: str | None = Field(None, alias="contentOwner")
    time_linked: datetime | None = Field(None, alias="timeLinked")


class Channel(BaseModel):
    """A YouTube channel resource."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    kind: Literal["youtube#channel"] = Field(default="youtube#channel")
    etag: str | None = None
    id: str | None = None
    snippet: ChannelSnippet | None = None
    content_details: ContentDetails | None = Field(None, alias="contentDetails")
    statistics: Statistics | None = None
    topic_details: TopicDetails | None = Field(None, alias="topicDetails")
    status: Status | None = None
    branding_settings: BrandingSettings | None = Field(None, alias="brandingSettings")
    audit_details: AuditDetails | None = Field(None, alias="auditDetails")
    content_owner_details: ContentOwnerDetails | None = Field(
        None, alias="contentOwnerDetails"
    )
    localizations: Dict[str, Localized] | None = None


class ListAllChannelsRequest(BaseModel):
    """Request parameters for listing all channels from the YouTube Data API channels.list endpoint."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    part: list[ChannelPart] = Field(
        description="List of channel resource properties to include in the response",
    )

    # Internal configuration for serialization behavior
    _serialize_part_as_string: bool = False

    # Filter parameters (exactly one must be specified)
    for_handle: str | None = Field(
        None, alias="forHandle", description="YouTube handle (can include @ symbol)"
    )
    for_username: str | None = Field(
        None, alias="forUsername", description="YouTube username"
    )
    id: list[str] | None = Field(
        None, description="List of YouTube channel IDs or comma-separated string"
    )
    managed_by_me: bool | None = Field(
        None,
        alias="managedByMe",
        description="Return only channels managed by content owner",
    )
    mine: bool | None = Field(
        None, description="Return only channels owned by authenticated user"
    )

    # Optional parameters
    hl: str | None = Field(None, description="Language code for localized metadata")
    on_behalf_of_content_owner: str | None = Field(
        None,
        alias="onBehalfOfContentOwner",
        description="Content owner on whose behalf the request is made",
    )

    @field_validator("part", mode="before")
    @classmethod
    def validate_part(cls, v: Any):
        """Parse and validate part parameter - accepts string or list."""
        return validate_part(v, ChannelPart)

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: Any):
        """Parse and validate id parameter - accepts string or list."""
        return validate_id(v)

    @field_serializer("part")
    def serialize_part(self, v: list[str]) -> str | list[str]:
        """Serialize part list to comma-separated string or keep as list based on configuration."""
        if self._serialize_part_as_string:
            return ",".join(v)
        return v

    @field_serializer("id")
    def serialize_id(self, v: list[str] | None) -> str | list[str] | None:
        """Serialize id list to comma-separated string or keep as list based on configuration."""
        if v is None:
            return v
        if self._serialize_part_as_string:
            return ",".join(v)
        return v

    @field_validator("for_handle")
    @classmethod
    def validate_for_handle(cls, v):
        """Allow @ symbol to be optional in handle."""
        if v and not v.startswith("@"):
            return f"@{v}"
        return v

    def __init__(self, **data):
        super().__init__(**data)
        # Validate that exactly one filter parameter is specified
        filter_params = [
            self.for_handle,
            self.for_username,
            self.id,
            self.managed_by_me,
            self.mine,
        ]
        specified_filters = [p for p in filter_params if p is not None]

        if len(specified_filters) != 1:
            raise ValueError(
                "Exactly one filter parameter must be specified: forHandle, forUsername, id, managedByMe, or mine"
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


class ListAllChannelsResponse(BaseModel):
    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    kind: Literal["youtube#channelListResponse"] = Field(
        default="youtube#channelListResponse"
    )
    items: List[Channel] = Field(default_factory=list)


class ListChannelsRequest(ListAllChannelsRequest, ListRequestMixin):
    """Request parameters for the YouTube Data API channels.list endpoint."""

    max_results: int | None = Field(
        None,
        alias="maxResults",
        ge=0,
        le=50,
        description="Maximum number of results (0-50, default 5)",
    )


class ListChannelsResponse(ListAllChannelsResponse, ListResponseMixin):
    pass
