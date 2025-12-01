import restate

from .executor import Executor
from .model import (
    ListChannelsRequest,
    ListChannelsResponse,
    ListPlaylistsRequest,
    ListPlaylistsResponse,
)


def create_service(
    executor: Executor,
    service_name: str = "YouTube",
) -> restate.Service:
    service = restate.Service(service_name)

    register_service(executor, service)

    return service


def register_service(
    executor: Executor,
    service: restate.Service,
):
    @service.handler("listChannels")
    async def list_channels(
        ctx: restate.Context,
        request: ListChannelsRequest,
    ) -> ListChannelsResponse:
        return await ctx.run_typed(
            "list_channels",
            executor.list_channels,
            request=request,
        )

    @service.handler("listPlaylists")
    async def list_playlists(
        ctx: restate.Context,
        request: ListPlaylistsRequest,
    ) -> ListPlaylistsResponse:
        return await ctx.run_typed(
            "list_playlists",
            executor.list_playlists,
            request=request,
        )
