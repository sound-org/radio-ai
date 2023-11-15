package channel

import (
	"fmt"
	"path/filepath"
	"sync"
	"time"

	"github.com/sound-org/radio-ai/server/internal/hls"
	"github.com/sound-org/radio-ai/server/pkg/utils"
)

type Channel struct {
	src      string
	cache    *Cache
	streamer *Streamer
}

func CreateChannel(src string) *Channel {

	cacheMutex := sync.RWMutex{}
	streamerMutex := sync.RWMutex{}

	cache := CreateCache(src, &cacheMutex)
	streamer := CreateStreamer(getStreamingFile(), &streamerMutex)

	return &Channel{
		src:      src,
		cache:    cache,
		streamer: streamer,
	}
}

func getStreamingFile() *hls.Playlist {
	// TODO : add read values from configuration
	return &hls.Playlist{
		Metadata: hls.Metadata{
			Version:  3,
			Sequence: 0,
			Cache:    "NO",
			Duration: 11,
		},
		Ts:       []hls.TsFile{},
		HasEnd:   false,
		ToDelete: false,
	}
}

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

func Run(channel *Channel, quit *chan bool) {
	// TODO : initialize channel
	// TODO : start routinge for cache update
	// (?)TODO : start routine for cache delete

	err := channel.init()
	if err != nil {
		panic(err)
	}

	stream := time.NewTicker(10 * time.Second)
	go startUpdating(channel, stream, quit)
	// cacheUpdate := time.NewTicker(30 * time.Second)

}

func startUpdating(channel *Channel, ticker *time.Ticker, quit *chan bool) {
	current := 0
	// TODO : fow to get  offset for the 1st time?
	offset := maxBuffer
	next := channel.cache.Keys()
	// TODO : Fix to be less specific than this demo
	if len(next) < 2 {
		panic(fmt.Errorf("cache init failure"))
	}
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
				current = (current + 1) % 2
				offset = 0
				hls, err = channel.cache.Get(next[current])
				if err != nil {
					ticker.Stop()
					panic(err)
				}
				hls = mapTs(next[current], &hls)
			} else {
				current = current + pushSize
				offset = offset + pushSize
			}

		case <-*quit:
			ticker.Stop()
			return
		}
	}
}

func (channel *Channel) Stream() hls.Playlist {
	return channel.streamer.Get()
}

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
