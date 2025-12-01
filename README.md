# YouTube Restate service

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/sagikazarmark/restate-youtube/ci.yaml?style=flat-square)
![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/sagikazarmark/restate-youtube/badge?style=flat-square)

**A Restate service for the [YouTube Data API](https://developers.google.com/youtube/v3).**

This service provides Restate-compatible endpoints for interacting with YouTube's Data API, including support for channels, playlists, playlist items, and videos.

## Features

- **Channels**: List and retrieve channel information
- **Playlists**: List and retrieve playlist information
- **Playlist Items**: List and retrieve playlist item information
- **Videos**: List and retrieve video information with comprehensive metadata

## API Endpoints

### Videos

#### `listVideos`
Returns a paginated list of videos that match the API request parameters.

**Parameters:**
- `part`: Array of video resource properties to include (required)
- Filter (exactly one required):
  - `id`: Comma-separated list of video IDs
  - `chart`: Chart type (`mostPopular`)
  - `myRating`: Videos liked/disliked by authenticated user (`like` or `dislike`)
- Optional parameters:
  - `maxResults`: Maximum number of results (1-50, not supported with `id` filter)
  - `pageToken`: Token for pagination
  - `regionCode`: Country code for chart filtering
  - `videoCategoryId`: Category ID for chart filtering
  - `hl`: Language code for localized metadata
  - `maxHeight`, `maxWidth`: Player dimensions (72-8192)

#### `listAllVideos`
Returns all videos matching the request parameters, automatically handling pagination.

**Example Usage:**

```python
from restate_youtube import ListVideosRequest, VideoPart, Chart

# Get specific videos by ID
request = ListVideosRequest(
    part=[VideoPart.SNIPPET, VideoPart.STATISTICS],
    id=["dQw4w9WgXcQ", "jNQXAC9IVRw"]
)

# Get most popular videos
request = ListVideosRequest(
    part=[VideoPart.SNIPPET, VideoPart.STATISTICS],
    chart=Chart.MOST_POPULAR,
    region_code="US",
    max_results=10
)
```

### Channels

#### `listChannels`
Returns a paginated list of channels.

#### `listAllChannels`
Returns all channels matching the request parameters.

### Playlists

#### `listPlaylists`
Returns a paginated list of playlists.

#### `listAllPlaylists`
Returns all playlists matching the request parameters.

### Playlist Items

#### `listPlaylistItems`
Returns a paginated list of playlist items.

#### `listAllPlaylistItems`
Returns all playlist items matching the request parameters.

## Setup

1. Get a YouTube Data API key from the [Google Cloud Console](https://console.cloud.google.com/apis/dashboard)
2. Set the `GOOGLE_API_KEY` environment variable
3. Run the service

## License

The project is licensed under the [MIT License](LICENSE).
