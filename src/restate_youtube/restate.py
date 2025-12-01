import restate

from .executor import Executor
from .model_channels import (
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
)
from .model_playlists import (
    ListAllPlaylistsRequest,
    ListAllPlaylistsResponse,
    ListPlaylistsRequest,
    ListPlaylistsResponse,
)
from .model_videos import (
    ListAllVideosRequest,
    ListAllVideosResponse,
    ListVideosRequest,
    ListVideosResponse,
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

    @service.handler("listVideos")
    async def list_videos(
        ctx: restate.Context,
        request: ListVideosRequest,
    ) -> ListVideosResponse:
        return await ctx.run_typed(
            "list_videos",
            executor.list_videos,
            request=request,
        )

    @service.handler("listAllVideos")
    async def list_all_videos(
        ctx: restate.Context,
        request: ListAllVideosRequest,
    ) -> ListAllVideosResponse:
        return await ctx.run_typed(
            "list_all_videos",
            executor.list_all_videos,
            request=request,
        )
