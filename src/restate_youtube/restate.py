import restate

from .executor import Executor
from .model import (
    ListAllChannelsRequest,
    ListAllChannelsResponse,
    ListAllPlaylistItemsRequest,
    ListAllPlaylistItemsResponse,
    ListAllPlaylistsRequest,
    ListAllPlaylistsResponse,
    ListChannelsRequest,
    ListChannelsResponse,
    ListPlaylistItemsRequest,
    ListPlaylistItemsResponse,
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

    @service.handler("listAllPlaylists")
    async def list_all_playlists(
        ctx: restate.Context,
        request: ListAllPlaylistsRequest,
    ) -> ListAllPlaylistsResponse:
        return await ctx.run_typed(
            "list_all_playlists",
            executor.list_all_playlists,
            request=request,
        )

    @service.handler("listAllChannels")
    async def list_all_channels(
        ctx: restate.Context,
        request: ListAllChannelsRequest,
    ) -> ListAllChannelsResponse:
        return await ctx.run_typed(
            "list_all_channels",
            executor.list_all_channels,
            request=request,
        )

    @service.handler("listPlaylistItems")
    async def list_playlist_items(
        ctx: restate.Context,
        request: ListPlaylistItemsRequest,
    ) -> ListPlaylistItemsResponse:
        return await ctx.run_typed(
            "list_playlist_items",
            executor.list_playlist_items,
            request=request,
        )

    @service.handler("listAllPlaylistItems")
    async def list_all_playlist_items(
        ctx: restate.Context,
        request: ListAllPlaylistItemsRequest,
    ) -> ListAllPlaylistItemsResponse:
        return await ctx.run_typed(
            "list_all_playlist_items",
            executor.list_all_playlist_items,
            request=request,
        )
