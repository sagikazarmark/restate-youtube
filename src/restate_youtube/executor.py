import logging
from typing import List

from .model_channels import (
    Channel,
    ListAllChannelsRequest,
    ListAllChannelsResponse,
    ListChannelsRequest,
    ListChannelsResponse,
)
from .model_playlist_item import (
    ListAllPlaylistItemsRequest,
    ListAllPlaylistItemsResponse,
    ListPlaylistItemsRequest,
    ListPlaylistItemsResponse,
    PlaylistItem,
)
from .model_playlists import (
    ListAllPlaylistsRequest,
    ListAllPlaylistsResponse,
    ListPlaylistsRequest,
    ListPlaylistsResponse,
    Playlist,
)
from .model_videos import (
    ListAllVideosRequest,
    ListAllVideosResponse,
    ListVideosRequest,
    ListVideosResponse,
    Video,
)

_logger = logging.getLogger(__name__)


class Executor:
    def __init__(
        self,
        youtube,
        logger: logging.Logger = _logger,
    ):
        self.youtube = youtube
        self.logger = logger

    def list_channels(self, request: ListChannelsRequest) -> ListChannelsResponse:
        apiRequest = self.youtube.channels().list(
            **request.model_dump(
                exclude_none=True,
                context={"comma_separated": True},
            ),
        )
        apiResponse = apiRequest.execute()

        return ListChannelsResponse.model_validate(apiResponse)

    def list_all_channels(
        self,
        request: ListAllChannelsRequest,
    ) -> ListAllChannelsResponse:
        items: List[Channel] = []
        next_page_token = None

        while True:
            apiRequest = self.youtube.channels().list(
                pageToken=next_page_token,
                maxResults=50,
                **request.model_dump(
                    exclude_none=True,
                    context={"comma_separated": True},
                ),
            )
            response = apiRequest.execute()

            items.extend(response["items"])

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return ListAllChannelsResponse(items=items)

    def list_playlists(self, request: ListPlaylistsRequest) -> ListPlaylistsResponse:
        apiRequest = self.youtube.playlists().list(
            **request.model_dump(
                exclude_none=True,
                context={"comma_separated": True},
            ),
        )
        apiResponse = apiRequest.execute()

        return ListPlaylistsResponse.model_validate(apiResponse)

    def list_all_playlists(
        self,
        request: ListAllPlaylistsRequest,
    ) -> ListAllPlaylistsResponse:
        items: List[Playlist] = []
        next_page_token = None

        while True:
            apiRequest = self.youtube.playlists().list(
                pageToken=next_page_token,
                maxResults=50,
                **request.model_dump(
                    exclude_none=True,
                    context={"comma_separated": True},
                ),
            )
            response = apiRequest.execute()

            items.extend(response["items"])

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return ListAllPlaylistsResponse(items=items)

    def list_playlist_items(
        self, request: ListPlaylistItemsRequest
    ) -> ListPlaylistItemsResponse:
        apiRequest = self.youtube.playlistItems().list(
            **request.model_dump(
                exclude_none=True,
                context={"comma_separated": True},
            ),
        )
        apiResponse = apiRequest.execute()

        return ListPlaylistItemsResponse.model_validate(apiResponse)

    def list_all_playlist_items(
        self,
        request: ListAllPlaylistItemsRequest,
    ) -> ListAllPlaylistItemsResponse:
        items: List[PlaylistItem] = []
        next_page_token = None

        while True:
            apiRequest = self.youtube.playlistItems().list(
                pageToken=next_page_token,
                maxResults=50,
                **request.model_dump(
                    exclude_none=True,
                    context={"comma_separated": True},
                ),
            )
            response = apiRequest.execute()

            items.extend(response["items"])

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return ListAllPlaylistItemsResponse(items=items)

    def list_videos(self, request: ListVideosRequest) -> ListVideosResponse:
        apiRequest = self.youtube.videos().list(
            **request.model_dump(
                exclude_none=True,
                context={"comma_separated": True},
            ),
        )
        apiResponse = apiRequest.execute()

        return ListVideosResponse.model_validate(apiResponse)

    def list_all_videos(
        self,
        request: ListAllVideosRequest,
    ) -> ListAllVideosResponse:
        items: List[Video] = []
        next_page_token = None
        max_results = 50

        if request.id is not None:
            max_results = None

        while True:
            apiRequest = self.youtube.videos().list(
                pageToken=next_page_token,
                maxResults=max_results,
                **request.model_dump(
                    exclude_none=True,
                    context={"comma_separated": True},
                ),
            )
            response = apiRequest.execute()

            items.extend(response["items"])

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return ListAllVideosResponse(items=items)
