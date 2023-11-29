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

type Channel struct {
	Config   cnf.ChannelConfig
	cache    *Cache
	streamer *Streamer
}

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

func startUpdating(channel *Channel, ticker *time.Ticker, quit *chan bool) {
	log.Printf("Channel(%d) \"%s\" running...\n", channel.Config.Id, channel.Config.Desc)
	current := 0
	// TODO : fow to get  offset for the 1st time?
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

func startRefreshing(channel *Channel, ticker *time.Ticker, quit *chan bool) {

	for {
		select {
		case <-ticker.C:
			channel.cache.Refresh()
			log.Printf("Channel(%v) Refreshed\n", channel.Config.Id)
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
	log.Printf("[DEBUG] Mapping %s to %s\n", path, filepath.Base(path))
	return hls.Playlist{
		Metadata: playlist.Metadata,
		ToDelete: playlist.ToDelete,
		HasEnd:   playlist.HasEnd,
		Ts: utils.Map[hls.TsFile, hls.TsFile](playlist.Ts, func(ts hls.TsFile) hls.TsFile {
			return hls.TsFile{
				Header: ts.Header,
				Name:   filepath.ToSlash(filepath.Join(filepath.Base(path), ts.Name)),
			}
		}),
	}
}
