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
    PrivacyStatus,
    Thumbnails,
    validate_id,
    validate_part,
)


class VideoPart(str, Enum):
    """Video resource parts that can be included in API responses."""

    CONTENT_DETAILS = "contentDetails"
    FILE_DETAILS = "fileDetails"
    ID = "id"
    LIVE_STREAMING_DETAILS = "liveStreamingDetails"
    LOCALIZATIONS = "localizations"
    PAID_PRODUCT_PLACEMENT_DETAILS = "paidProductPlacementDetails"
    PLAYER = "player"
    PROCESSING_DETAILS = "processingDetails"
    RECORDING_DETAILS = "recordingDetails"
    SNIPPET = "snippet"
    STATISTICS = "statistics"
    STATUS = "status"
    SUGGESTIONS = "suggestions"
    TOPIC_DETAILS = "topicDetails"


class LiveBroadcastContent(str, Enum):
    """Live broadcast content status."""

    LIVE = "live"
    NONE = "none"
    UPCOMING = "upcoming"


class Dimension(str, Enum):
    """Video dimension (2D or 3D)."""

    TWO_D = "2d"
    THREE_D = "3d"


class Definition(str, Enum):
    """Video definition quality."""

    HD = "hd"
    SD = "sd"


class Caption(str, Enum):
    """Caption availability."""

    FALSE = "false"
    TRUE = "true"


class Projection(str, Enum):
    """Video projection format."""

    RECTANGULAR = "rectangular"
    THREE_SIXTY = "360"


class UploadStatus(str, Enum):
    """Video upload status."""

    DELETED = "deleted"
    FAILED = "failed"
    PROCESSED = "processed"
    REJECTED = "rejected"
    UPLOADED = "uploaded"


class License(str, Enum):
    """Video license."""

    CREATIVE_COMMON = "creativeCommon"
    YOUTUBE = "youtube"


class ProcessingStatus(str, Enum):
    """Video processing status."""

    FAILED = "failed"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    TERMINATED = "terminated"


class Chart(str, Enum):
    """Available video charts."""

    MOST_POPULAR = "mostPopular"


class MyRating(str, Enum):
    """User rating filter options."""

    DISLIKE = "dislike"
    LIKE = "like"


class VideoSnippet(BaseModel):
    """Basic details about the video."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    published_at: datetime | None = Field(default=None, alias="publishedAt")
    channel_id: str | None = Field(None, alias="channelId")
    title: str
    description: str
    thumbnails: Thumbnails | None = None
    channel_title: str | None = Field(None, alias="channelTitle")
    tags: List[str] | None = None
    category_id: str | None = Field(None, alias="categoryId")
    live_broadcast_content: LiveBroadcastContent | None = Field(
        None, alias="liveBroadcastContent"
    )
    default_language: str | None = Field(None, alias="defaultLanguage")
    localized: Localized | None = None
    default_audio_language: str | None = Field(None, alias="defaultAudioLanguage")


class RegionRestriction(BaseModel):
    """Region restriction information."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    allowed: List[str] | None = None
    blocked: List[str] | None = None


class VideoContentDetails(BaseModel):
    """Video content details."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    duration: str | None = None
    dimension: Dimension | None = None
    definition: Definition | None = None
    caption: Caption | None = None
    licensed_content: bool | None = Field(None, alias="licensedContent")
    region_restriction: RegionRestriction | None = Field(
        None, alias="regionRestriction"
    )
    projection: Projection | None = None
    has_custom_thumbnail: bool | None = Field(None, alias="hasCustomThumbnail")


class VideoStatus(BaseModel):
    """Video status information."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    upload_status: UploadStatus | None = Field(None, alias="uploadStatus")
    failure_reason: str | None = Field(None, alias="failureReason")
    rejection_reason: str | None = Field(None, alias="rejectionReason")
    privacy_status: PrivacyStatus | None = Field(None, alias="privacyStatus")
    publish_at: datetime | None = Field(None, alias="publishAt")
    license: License | None = None
    embeddable: bool | None = None
    public_stats_viewable: bool | None = Field(None, alias="publicStatsViewable")
    made_for_kids: bool | None = Field(None, alias="madeForKids")
    self_declared_made_for_kids: bool | None = Field(
        None, alias="selfDeclaredMadeForKids"
    )
    contains_synthetic_media: bool | None = Field(None, alias="containsSyntheticMedia")


class VideoStatistics(BaseModel):
    """Video statistics."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    view_count: str | None = Field(None, alias="viewCount")
    like_count: str | None = Field(None, alias="likeCount")
    dislike_count: str | None = Field(None, alias="dislikeCount")
    favorite_count: str | None = Field(None, alias="favoriteCount")
    comment_count: str | None = Field(None, alias="commentCount")


class PaidProductPlacementDetails(BaseModel):
    """Paid product placement details."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    has_paid_product_placement: bool | None = Field(
        None, alias="hasPaidProductPlacement"
    )


class VideoPlayer(BaseModel):
    """Video player information."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    embed_html: str | None = Field(None, alias="embedHtml")
    embed_height: int | None = Field(None, alias="embedHeight")
    embed_width: int | None = Field(None, alias="embedWidth")


class VideoTopicDetails(BaseModel):
    """Video topic details."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    topic_ids: List[str] | None = Field(None, alias="topicIds")
    relevant_topic_ids: List[str] | None = Field(None, alias="relevantTopicIds")
    topic_categories: List[str] | None = Field(None, alias="topicCategories")


class VideoRecordingDetails(BaseModel):
    """Video recording details."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    recording_date: datetime | None = Field(None, alias="recordingDate")


class VideoStream(BaseModel):
    """Video stream information."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    width_pixels: int | None = Field(None, alias="widthPixels")
    height_pixels: int | None = Field(None, alias="heightPixels")
    frame_rate_fps: float | None = Field(None, alias="frameRateFps")
    aspect_ratio: float | None = Field(None, alias="aspectRatio")
    codec: str | None = None
    bitrate_bps: int | None = Field(None, alias="bitrateBps")
    rotation: str | None = None
    vendor: str | None = None


class AudioStream(BaseModel):
    """Audio stream information."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    channel_count: int | None = Field(None, alias="channelCount")
    codec: str | None = None
    bitrate_bps: int | None = Field(None, alias="bitrateBps")
    vendor: str | None = None


class VideoFileDetails(BaseModel):
    """Video file details."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    file_name: str | None = Field(None, alias="fileName")
    file_size: int | None = Field(None, alias="fileSize")
    file_type: str | None = Field(None, alias="fileType")
    container: str | None = None
    video_streams: List[VideoStream] | None = Field(None, alias="videoStreams")
    audio_streams: List[AudioStream] | None = Field(None, alias="audioStreams")
    duration_ms: int | None = Field(None, alias="durationMs")
    bitrate_bps: int | None = Field(None, alias="bitrateBps")
    creation_time: str | None = Field(None, alias="creationTime")


class ProcessingProgress(BaseModel):
    """Video processing progress."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    parts_total: int | None = Field(None, alias="partsTotal")
    parts_processed: int | None = Field(None, alias="partsProcessed")
    time_left_ms: int | None = Field(None, alias="timeLeftMs")


class VideoProcessingDetails(BaseModel):
    """Video processing details."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    processing_status: ProcessingStatus | None = Field(None, alias="processingStatus")
    processing_progress: ProcessingProgress | None = Field(
        None, alias="processingProgress"
    )
    processing_failure_reason: str | None = Field(None, alias="processingFailureReason")
    file_details_availability: str | None = Field(None, alias="fileDetailsAvailability")
    processing_issues_availability: str | None = Field(
        None, alias="processingIssuesAvailability"
    )
    tag_suggestions_availability: str | None = Field(
        None, alias="tagSuggestionsAvailability"
    )
    editor_suggestions_availability: str | None = Field(
        None, alias="editorSuggestionsAvailability"
    )
    thumbnails_availability: str | None = Field(None, alias="thumbnailsAvailability")


class TagSuggestion(BaseModel):
    """Tag suggestion."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    tag: str
    category_restricts: List[str] | None = Field(None, alias="categoryRestricts")


class VideoSuggestions(BaseModel):
    """Video suggestions."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    processing_errors: List[str] | None = Field(None, alias="processingErrors")
    processing_warnings: List[str] | None = Field(None, alias="processingWarnings")
    processing_hints: List[str] | None = Field(None, alias="processingHints")
    tag_suggestions: List[TagSuggestion] | None = Field(None, alias="tagSuggestions")
    editor_suggestions: List[str] | None = Field(None, alias="editorSuggestions")


class VideoLiveStreamingDetails(BaseModel):
    """Live streaming details."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    actual_start_time: datetime | None = Field(None, alias="actualStartTime")
    actual_end_time: datetime | None = Field(None, alias="actualEndTime")
    scheduled_start_time: datetime | None = Field(None, alias="scheduledStartTime")
    scheduled_end_time: datetime | None = Field(None, alias="scheduledEndTime")
    concurrent_viewers: int | None = Field(None, alias="concurrentViewers")
    active_live_chat_id: str | None = Field(None, alias="activeLiveChatId")


class Video(BaseModel):
    """A YouTube video resource."""

    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    kind: Literal["youtube#video"] = Field(default="youtube#video")
    etag: str | None = None
    id: str | None = None
    snippet: VideoSnippet | None = None
    content_details: VideoContentDetails | None = Field(None, alias="contentDetails")
    status: VideoStatus | None = None
    statistics: VideoStatistics | None = None
    paid_product_placement_details: PaidProductPlacementDetails | None = Field(
        None, alias="paidProductPlacementDetails"
    )
    player: VideoPlayer | None = None
    topic_details: VideoTopicDetails | None = Field(None, alias="topicDetails")
    recording_details: VideoRecordingDetails | None = Field(
        None, alias="recordingDetails"
    )
    file_details: VideoFileDetails | None = Field(None, alias="fileDetails")
    processing_details: VideoProcessingDetails | None = Field(
        None, alias="processingDetails"
    )
    suggestions: VideoSuggestions | None = None
    live_streaming_details: VideoLiveStreamingDetails | None = Field(
        None, alias="liveStreamingDetails"
    )
    localizations: Dict[str, Localized] | None = None


class ListAllVideosRequest(BaseModel):
    """Request parameters for the YouTube Data API videos.list endpoint."""

    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)

    part: list[VideoPart] = Field(
        description="List of video resource properties to include in the response",
    )

    @field_validator("part", mode="before")
    def validate_part(cls, v: Any):
        return validate_part(v, VideoPart)

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
    chart: Chart | None = Field(
        None,
        description="Chart to retrieve (e.g., mostPopular)",
    )

    id: list[str] | None = Field(
        None,
        description="List of YouTube video IDs or comma-separated string",
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

    my_rating: MyRating | None = Field(
        None,
        alias="myRating",
        description="Return videos liked or disliked by authenticated user",
    )

    @model_validator(mode="after")
    def validate_exactly_one_filter(self):
        filter_fields = ["chart", "id", "my_rating"]
        specified = [f for f in filter_fields if getattr(self, f) is not None]

        if len(specified) != 1:
            raise ValueError(
                "Exactly one filter must be specified: "
                "chart, id, myRating. "
                f"Got: {specified or 'none'}"
            )

        return self

    # Optional parameters
    hl: str | None = Field(None, description="Language code for localized metadata")
    max_height: int | None = Field(
        None,
        alias="maxHeight",
        ge=72,
        le=8192,
        description="Maximum height for embedded player (72-8192)",
    )
    max_width: int | None = Field(
        None,
        alias="maxWidth",
        ge=72,
        le=8192,
        description="Maximum width for embedded player (72-8192)",
    )
    on_behalf_of_content_owner: str | None = Field(
        None,
        alias="onBehalfOfContentOwner",
        description="Content owner on whose behalf the request is made",
    )
    region_code: str | None = Field(
        None,
        alias="regionCode",
        description="ISO 3166-1 alpha-2 country code for chart filtering",
    )
    video_category_id: str | None = Field(
        None,
        alias="videoCategoryId",
        description="Video category ID for chart filtering (default: 0)",
    )


class ListAllVideosResponse(BaseModel):
    model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    kind: Literal["youtube#videoListResponse"] = Field(
        default="youtube#videoListResponse"
    )
    items: List[Video] = Field(default_factory=list)


class ListVideosRequest(ListAllVideosRequest, ListRequestMixin):
    max_results: int | None = Field(
        None,
        alias="maxResults",
        ge=1,
        le=50,
        description="Maximum number of results (1-50, default 5). Not supported with id filter.",
    )

    @model_validator(mode="after")
    def validate_max_results_compatibility(self):
        # maxResults is not supported with id parameter
        if self.id is not None and self.max_results is not None:
            raise ValueError("maxResults parameter is not supported with id filter")

        return self


class ListVideosResponse(ListAllVideosResponse, ListResponseMixin):
    pass
