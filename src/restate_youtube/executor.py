import logging
from typing import List

from .model import (
    ListAllPlaylistsRequest,
    ListAllPlaylistsResponse,
    ListChannelsRequest,
    ListChannelsResponse,
    ListPlaylistsRequest,
    ListPlaylistsResponse,
    Playlist,
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
            **request.model_dump_for_api(exclude_none=True)
        )
        apiResponse = apiRequest.execute()

        return ListChannelsResponse.model_validate(apiResponse)

    def list_playlists(self, request: ListPlaylistsRequest) -> ListPlaylistsResponse:
        apiRequest = self.youtube.playlists().list(
            **request.model_dump_for_api(exclude_none=True)
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
                **request.model_dump_for_api(exclude_none=True),
            )
            response = apiRequest.execute()

            items.extend(response["items"])

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return ListAllPlaylistsResponse(items=items)
