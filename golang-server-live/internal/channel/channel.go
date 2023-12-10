package channel

import (
	"fmt"
	"log"
	"path/filepath"
	"sync"
	"time"

	"github.com/sound-org/radio-ai/server/internal/cnf"
	"github.com/sound-org/radio-ai/server/internal/hls"
	"github.com/sound-org/radio-ai/server/pkg/utils"
)

// Channel represents a streaming channel with associated configuration, cache, and streamer.
type Channel struct {
	Config   cnf.ChannelConfig
	cache    *Cache
	streamer *Streamer
}

// FromConfig creates a Channel instance based on the provided ChannelConfig.
// It initializes a cache and a streamer using the configuration details.
//
// Parameters:
//   - cc: The ChannelConfig containing the configuration details for the channel.
//
// Returns:
//   - *Channel: A pointer to the created Channel instance.
//
// Example usage:
//
//	config := // initialize your ChannelConfig
//	myChannel := FromConfig(config)
func FromConfig(cc cnf.ChannelConfig) *Channel {

	cacheMutex := sync.RWMutex{}
	streamerMutex := sync.RWMutex{}

	streamer := CreateStreamer(&cc.Stream, &streamerMutex)
	cache := CreateCache(cc.Src, &cacheMutex)

	return &Channel{
		Config:   cc,
		cache:    cache,
		streamer: streamer,
	}
}

// init initializes the Channel by refreshing the cache, retrieving the playlist,
// mapping .ts files, and initializing the streamer.
//
// Returns:
//   - error: An error, if any, encountered during the initialization process.
//
// Example usage:
//
//	myChannel := // initialize your Channel
//	err := myChannel.init()
//	if err != nil {
//	    // handle the error
//	}
func (channel *Channel) init() error {
	err := channel.cache.Refresh()
	if err != nil {
		return err
	}

	keys := channel.cache.Keys()
	if len(keys) == 0 {
		return fmt.Errorf("cache was empty")
	}

	playlist, err := channel.cache.Get(keys[0])
	if err != nil {
		return err
	}
	playlist = mapTs(keys[0], &playlist)

	return channel.streamer.init(&playlist)
}

// Run starts the operations for a given channel, including initialization, updating, and refreshing.
//
// Parameters:
//   - channel: A pointer to the Channel instance to run operations on.
//   - quit:    A channel used for signaling when to stop the operations.
//
// Example usage:
//
//	myChannel := // initialize your Channel
//	quit := make(chan bool)
//	go Run(myChannel, &quit)
//	// Perform other operations...
//	// To stop the operations, close the 'quit' channel: close(quit)
func Run(channel *Channel, quit *chan bool) {

	log.Printf("[INIT] Channel(%d) \"%s\"\n", channel.Config.Id, channel.Config.Desc)

	err := channel.init()
	if err != nil {
		panic(err)
	}

	stream := time.NewTicker(10 * time.Second)
	go startUpdating(channel, stream, quit)

	refresh := time.NewTicker(20 * time.Second)
	go startRefreshing(channel, refresh, quit)
}

// startUpdating handles the periodic updating of the channel's streaming operations.
// It pushes chunks of the playlist to the streamer at a specified interval.
//
// Parameters:
//   - channel: A pointer to the Channel instance to update.
//   - ticker:  A time.Ticker controlling the update interval.
//   - quit:    A channel used for signaling when to stop the operations.
//
// Example usage:
//
//	myChannel := // initialize your Channel
//	ticker := time.NewTicker(10 * time.Second)
//	quit := make(chan bool)
//	go startUpdating(myChannel, ticker, &quit)
//	// Perform other operations...
//	// To stop the operations, close the 'quit' channel: close(quit)
func startUpdating(channel *Channel, ticker *time.Ticker, quit *chan bool) {
	log.Printf("[INFO] Channel(%d) \"%s\" running...\n", channel.Config.Id, channel.Config.Desc)
	current := 0
	offset := int(channel.Config.Stream.Buffer)
	next := channel.cache.Keys()

	hls, err := channel.cache.Get(next[current])
	if err != nil {
		panic(err)
	}
	hls = mapTs(next[current], &hls)
	for {
		select {
		case <-ticker.C:
			err := channel.streamer.Push(&hls, offset)
			if err != nil {
				// on error skip to next song
				current = (current + 1) % len(next)
				offset = 0
				hls, err = channel.cache.Get(next[current])
				if err != nil {
					ticker.Stop()
					panic(err)
				}
				hls = mapTs(next[current], &hls)
			} else {
				current = current + int(channel.Config.Stream.PushSize)
				offset = offset + int(channel.Config.Stream.PushSize)
			}

		case <-*quit:
			ticker.Stop()
			return
		}
	}
}

// startRefreshing handles the periodic refreshing of the channel's cache.
//
// Parameters:
//   - channel: A pointer to the Channel instance to refresh.
//   - ticker:  A time.Ticker controlling the refresh interval.
//   - quit:    A channel used for signaling when to stop the operations.
//
// Example usage:
//
//	myChannel := // initialize your Channel
//	ticker := time.NewTicker(20 * time.Second)
//	quit := make(chan bool)
//	go startRefreshing(myChannel, ticker, &quit)
//	// Perform other operations...
//	// To stop the operations, close the 'quit' channel: close(quit)
func startRefreshing(channel *Channel, ticker *time.Ticker, quit *chan bool) {

	for {
		select {
		case <-ticker.C:
			channel.cache.Refresh()
			log.Printf("[INFO] Channel(%v) refreshed\n", channel.Config.Id)
		case <-*quit:
			ticker.Stop()
			return
		}
	}
}

// Stream retrieves the current playlist from the Channel's streamer.
//
// Returns:
//   - hls.Playlist: The current playlist for streaming.
//
// Example usage:
//
//	myChannel := // initialize your Channel
//	playlist := myChannel.Stream()
func (channel *Channel) Stream() hls.Playlist {
	return channel.streamer.Get()
}

// mapTs maps the file paths in the playlist to the specified directory path.
//
// Parameters:
//   - path:     The base directory path to map to the playlist files.
//   - playlist: A pointer to the original playlist to map.
//
// Returns:
//   - hls.Playlist: A new playlist with mapped file paths.
//
// Example usage:
//
//	baseDirectory := "/path/to/files"
//	originalPlaylist := // initialize your Playlist
//	mappedPlaylist := mapTs(baseDirectory, &originalPlaylist)
func mapTs(path string, playlist *hls.Playlist) hls.Playlist {
	return hls.Playlist{
		Metadata: playlist.Metadata,
		ToDelete: playlist.ToDelete,
		HasEnd:   playlist.HasEnd,
		Ts: utils.Map[hls.TsFile, hls.TsFile](playlist.Ts, func(ts hls.TsFile) hls.TsFile {
			return hls.TsFile{
				Header: ts.Header,
				Name:   filepath.ToSlash(filepath.Join(path, ts.Name)),
			}
		}),
	}
}
