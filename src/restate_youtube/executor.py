import logging

from .model import (
    ListChannelsRequest,
    ListChannelsResponse,
    ListPlaylistsRequest,
    ListPlaylistsResponse,
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
        print(request.model_dump_for_api(exclude_none=True))
        apiRequest = self.youtube.channels().list(
            **request.model_dump_for_api(exclude_none=True)
        )
        apiResponse = apiRequest.execute()

        return ListChannelsResponse.model_validate(apiResponse)

    def list_playlists(self, request: ListPlaylistsRequest) -> ListPlaylistsResponse:
        print(request.model_dump_for_api(exclude_none=True))
        apiRequest = self.youtube.playlists().list(
            **request.model_dump_for_api(exclude_none=True)
        )
        apiResponse = apiRequest.execute()

        return ListPlaylistsResponse.model_validate(apiResponse)
