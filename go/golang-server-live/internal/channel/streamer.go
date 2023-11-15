package channel

import (
	"fmt"
	"sync"

	"github.com/sound-org/radio-ai/server/internal/hls"
)

// should be constant
const maxBuffer = 10
const pushSize = 2

type Streamer struct {
	Stream *hls.Playlist
	mutex  *sync.RWMutex
}

func CreateStreamer(playlits *hls.Playlist, mutex *sync.RWMutex) *Streamer {
	return &Streamer{
		Stream: playlits,
		mutex:  mutex,
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

	end := min(len(file.Ts), start+pushSize)
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

	size := min(len(file.Ts), maxBuffer)
	streamer.Stream.Ts = append(streamer.Stream.Ts, file.Ts[0:size]...)
	return nil
}

func (streamer *Streamer) Get() hls.Playlist {
	streamer.mutex.RLock()
	defer streamer.mutex.RUnlock()
	return *streamer.Stream
}
