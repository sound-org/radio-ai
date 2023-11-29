package streaming_test

import (
	"log"
	"os"
	"sync"
	"testing"

	"github.com/sound-org/radio-ai/server/internal/channel"
	"github.com/sound-org/radio-ai/server/internal/cnf"
	"github.com/sound-org/radio-ai/server/internal/hls"
	test_utils "github.com/sound-org/radio-ai/server/internal/utils"
)

func getHlsConfig() cnf.HlsConfig {
	return cnf.HlsConfig{
		Buffer:   10,
		PushSize: 2,
		Version:  3,
		Sequence: 0,
		Duration: 11,
		Cache:    false,
	}

}

func TestCreateStreamer(t *testing.T) {
	config := getHlsConfig()
	streamer := channel.CreateStreamer(&config, &sync.RWMutex{})

	if streamer == nil {
		log.Fatal("Streamer was empty")
	}

	if (streamer.Stream.Metadata.Cache == "YES") ||
		(streamer.Stream.Metadata.Version != 3) ||
		(streamer.Stream.Metadata.Duration != 11) ||
		(streamer.Stream.Metadata.Sequence != 0) {
		log.Fatal("Streamer has not parsed config properly")
	}
}

func TestPust(t *testing.T) {
	config := getHlsConfig()
	streamer := channel.CreateStreamer(&config, &sync.RWMutex{})

	if streamer == nil {
		log.Fatal("Streamer was empty")
	}

	// fake initialization of TS in streamer
	streamer.Stream.Ts = make([]hls.TsFile, 10)

	file, err := test_utils.CreateFile(test_utils.GetM3U8(), ".", "test*.m3u8")
	if err != nil {
		log.Fatal(err)
	}
	defer os.Remove(file.Name())

	reader, err := os.Open(file.Name())
	if err != nil {
		log.Fatal(err)
	}
	defer reader.Close()

	rec, err := hls.Load(reader)
	if err != nil {
		log.Fatal(err)
	}

	err = streamer.Push(rec, 0)
	if err != nil {
		log.Fatal(err)
	}

	if len(streamer.Stream.Ts) != 10 {
		log.Fatal("Streamer should have 10 ts files added")
	}

	if streamer.Stream.Ts[8] != rec.Ts[0] {
		log.Fatal("Streamer should push fifo to Stream")
	}
}
