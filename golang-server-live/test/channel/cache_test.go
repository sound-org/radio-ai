package channel_test

import (
	"log"
	"os"
	"sync"
	"testing"

	"github.com/sound-org/radio-ai/server/internal/channel"
	test_utils "github.com/sound-org/radio-ai/server/internal/utils"
)

func TestCreateCache(t *testing.T) {
	cache := channel.CreateCache("root", &sync.RWMutex{})

	if cache == nil {
		log.Fatal("Cache is nil")
	}
}

func TestRefresh(t *testing.T) {
	cache := channel.CreateCache("./root", &sync.RWMutex{})

	if cache == nil {
		log.Fatal("Cache is nil")
	}

	err := os.MkdirAll("./root/channel/streaming/files", 0777)
	if err != nil {
		log.Fatal(err)
	}
	defer os.RemoveAll("./root")

	file, err := test_utils.CreateFile(test_utils.GetM3U8(), "./root/channel/streaming/files", "test*.m3u8")
	defer os.Remove(file.Name())
	if err != nil {
		log.Fatal(err)
	}

	err = cache.Refresh()
	if err != nil {
		log.Fatal(err)
	}

	if len(cache.Keys()) != 1 {
		log.Fatal("Cache was not refreshed")
	}
}

func TestKeysForEmptyCache(t *testing.T) {
	cache := channel.CreateCache("root", &sync.RWMutex{})

	if cache == nil {
		log.Fatal("Cache was nil")
	}

	keys := cache.Keys()
	if len(keys) != 0 {
		log.Fatal("Cahce should be empty")
	}
}

func TestKeys(t *testing.T) {
	cache := channel.CreateCache("root", &sync.RWMutex{})

	if cache == nil {
		log.Fatal("Cache was nil")
	}

	err := os.MkdirAll("./root/channel/streaming/files", 0777)
	if err != nil {
		log.Fatal(err)
	}
	err = os.MkdirAll("./root/channel/streaming/files2", 0777)
	if err != nil {
		log.Fatal(err)
	}
	defer os.RemoveAll("./root")

	file1, err := test_utils.CreateFile(test_utils.GetM3U8(), "./root/channel/streaming/files", "test*.m3u8")
	defer os.Remove(file1.Name())
	if err != nil {
		log.Fatal(err)
	}

	file2, err := test_utils.CreateFile(test_utils.GetM3U8(), "./root/channel/streaming/files2", "test*.m3u8")
	defer os.Remove(file2.Name())
	if err != nil {
		log.Fatal(err)
	}

	err = cache.Refresh()
	if err != nil {
		log.Fatal(err)
	}

	keys1 := cache.Keys()
	keys2 := cache.Keys()

	if keys1[0] != keys2[0] {
		log.Fatal("Caches keys should be deterministic")
	}
}

func TestGet(t *testing.T) {

	cache := channel.CreateCache("./root", &sync.RWMutex{})

	if cache == nil {
		log.Fatal("Cache is nil")
	}

	err := os.MkdirAll("./root/channel/streaming/files", 0777)
	if err != nil {
		log.Fatal(err)
	}
	defer os.RemoveAll("./root")

	file, err := test_utils.CreateFile(test_utils.GetM3U8(), "./root/channel/streaming/files", "test*.m3u8")
	defer os.Remove(file.Name())
	if err != nil {
		log.Fatal(err)
	}

	err = cache.Refresh()
	if err != nil {
		log.Fatal(err)
	}

	playlist, err := cache.Get("files")
	if err != nil {
		log.Fatal(err)
	}

	if len(playlist.Tags) != 5 {
		log.Fatal("Playlist should be 5 ts long")
	}
}
