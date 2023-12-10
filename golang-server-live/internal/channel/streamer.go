package channel

import (
	"fmt"
	"sync"

	"github.com/sound-org/radio-ai/server/internal/cnf"
	"github.com/sound-org/radio-ai/server/internal/hls"
)

// Streamer represents a sliding window for HLS protocol live streaming.
type Streamer struct {
	Stream *hls.Playlist
	config cnf.HlsConfig
	mutex  *sync.RWMutex
}

// CreateStreamer creates a new Streamer instance with the specified configuration and mutex.
//
// Parameters:
//   - config: A pointer to the HlsConfig containing the configuration details for the streamer.
//   - mutex:  A pointer to a sync.RWMutex used for concurrent access to the streamer.
//
// Returns:
//   - *Streamer: A pointer to the created Streamer instance.
//
// Example usage:
//
//	streamerConfig := // initialize your HlsConfig
//	streamerMutex := &sync.RWMutex{}
//	myStreamer := CreateStreamer(streamerConfig, streamerMutex)
func CreateStreamer(config *cnf.HlsConfig, mutex *sync.RWMutex) *Streamer {

	return &Streamer{
		Stream: getStreamingFile(config),
		config: *config,
		mutex:  mutex,
	}
}

// getStreamingFile creates a new streaming file (Playlist) based on the provided HlsConfig.
//
// Parameters:
//   - hc: A pointer to the HlsConfig containing the configuration details for the streaming file.
//
// Returns:
//   - *hls.Playlist: A pointer to the created Playlist instance representing the streaming file.
//
// Example usage:
//
//	streamerConfig := // initialize your HlsConfig
//	streamingFile := getStreamingFile(streamerConfig)
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

// Push adds a playlist to the streamer starting from the specified index.
// This operation is thread-safe as it acquires and releases a lock.
//
// Parameters:
//   - file:  A pointer to the Playlist to push into the streamer.
//   - start: The starting index in the playlist to begin pushing from.
//
// Returns:
//   - error: An error, if any, encountered during the push operation.
//
// Example usage:
//
//	myStreamer := // initialize your Streamer
//	myPlaylist := // initialize your Playlist
//	startIdx := 0
//	err := myStreamer.Push(myPlaylist, startIdx)
//	if err != nil {
//	    // handle the error
//	}
func (streamer *Streamer) Push(file *hls.Playlist, start int) error {

	streamer.mutex.Lock()
	defer streamer.mutex.Unlock()

	return streamer.push(file, start)
}

// push adds a portion of a playlist to the streamer, starting from the specified index.
// It updates the streamer's Ts slice and Sequence metadata accordingly.
//
// Parameters:
//   - file:  A pointer to the Playlist to push into the streamer.
//   - start: The starting index in the playlist to begin pushing from.
//
// Returns:
//   - error: An error, if any, encountered during the push operation.
//
// Example usage:
//
//	myStreamer := // initialize your Streamer
//	myPlaylist := // initialize your Playlist
//	startIdx := 0
//	err := myStreamer.push(myPlaylist, startIdx)
//	if err != nil {
//	    // handle the error
//	}
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

// init initializes the streamer with a portion of a playlist, up to the configured buffer size.
//
// Parameters:
//   - file: A pointer to the Playlist used to initialize the streamer.
//
// Returns:
//   - error: An error, if any, encountered during the initialization process.
//
// Example usage:
//
//	myStreamer := // initialize your Streamer
//	myPlaylist := // initialize your Playlist
//	err := myStreamer.init(myPlaylist)
//	if err != nil {
//	    // handle the error
//	}
func (streamer *Streamer) init(file *hls.Playlist) error {
	// initialize stream with at most maxBuffer of ts files from file
	if len(streamer.Stream.Ts) != 0 {
		return fmt.Errorf("empty playlist")
	}

	size := min(len(file.Ts), int(streamer.config.Buffer))
	streamer.Stream.Ts = append(streamer.Stream.Ts, file.Ts[0:size]...)
	return nil
}

// Get retrieves the current playlist from the streamer in a thread-safe manner.
//
// Returns:
//   - hls.Playlist: A copy of the current playlist in the streamer.
//
// Example usage:
//
//	myStreamer := // initialize your Streamer
//	currentPlaylist := myStreamer.Get()
func (streamer *Streamer) Get() hls.Playlist {
	streamer.mutex.RLock()
	defer streamer.mutex.RUnlock()
	return *streamer.Stream
}
