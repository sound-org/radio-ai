package channel

import (
	"fmt"
	"sync"

	"github.com/sound-org/radio-ai/server/internal/cnf"
	"github.com/sound-org/radio-ai/server/internal/hls"
)

type Streamer struct {
	Stream *hls.Playlist
	config cnf.HlsConfig
	mutex  *sync.RWMutex
}

func CreateStreamer(config *cnf.HlsConfig, mutex *sync.RWMutex) *Streamer {

	return &Streamer{
		Stream: getStreamingFile(config),
		config: *config,
		mutex:  mutex,
	}
}

func getStreamingFile(hc *cnf.HlsConfig) *hls.Playlist {

	cache := "NO"
	if hc.Cache {
		cache = "YES"
	}

	return &hls.Playlist{
		Metadata: hls.Metadata{
			Version:  uint16(hc.Version),
			Sequence: uint32(hc.Sequence),
			Cache:    cache,
			Duration: float32(hc.Duration),
		},
		Ts:       []hls.TsFile{},
		HasEnd:   false,
		ToDelete: false,
	}
}

func (streamer *Streamer) Push(file *hls.Playlist, start int) error {

	streamer.mutex.Lock()
	defer streamer.mutex.Unlock()

	return streamer.push(file, start)
}

func (streamer *Streamer) push(file *hls.Playlist, start int) error {
	if len(file.Ts) <= start {
		return fmt.Errorf("file out of index")
	}

	end := min(len(file.Ts), start+int(streamer.config.PushSize))
	size := end - start

	streamer.Stream.Ts = streamer.Stream.Ts[size:]
	streamer.Stream.Ts = append(streamer.Stream.Ts, file.Ts[start:end]...)
	streamer.Stream.Metadata.Sequence = streamer.Stream.Metadata.Sequence + uint32(size)

	return nil
}

func (streamer *Streamer) init(file *hls.Playlist) error {
	// initialize stream with at most maxBuffer of ts files from file
	if len(streamer.Stream.Ts) != 0 {
		return fmt.Errorf("empty playlist")
	}

	size := min(len(file.Ts), int(streamer.config.Buffer))
	streamer.Stream.Ts = append(streamer.Stream.Ts, file.Ts[0:size]...)
	return nil
}

func (streamer *Streamer) Get() hls.Playlist {
	streamer.mutex.RLock()
	defer streamer.mutex.RUnlock()
	return *streamer.Stream
}
