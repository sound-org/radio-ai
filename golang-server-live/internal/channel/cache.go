package channel

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"slices"
	"strings"
	"sync"

	"github.com/sound-org/radio-ai/server/internal/hls"
	"github.com/sound-org/radio-ai/server/pkg/utils"
)

// Cache represents a file system containing broadcasts in form of playlists and .ts files.
type Cache struct {
	src       string
	playlists map[string]*hls.Playlist
	mutex     *sync.RWMutex
}

// CreateCache creates a new Cache instance with the specified source directory and mutex.
//
// Parameters:
//   - src:   The source directory path for the cache.
//   - mutex: A pointer to a sync.RWMutex used for concurrent access to the cache.
//
// Returns:
//   - *Cache: A pointer to the created Cache instance.
//
// Example usage:
//
//	sourceDirectory := "/path/to/source"
//	cacheMutex := &sync.RWMutex{}
//	myCache := CreateCache(sourceDirectory, cacheMutex)
func CreateCache(src string, mutex *sync.RWMutex) *Cache {
	return &Cache{
		src:       src,
		playlists: make(map[string]*hls.Playlist),
		mutex:     mutex,
	}
}

// refresh updates the cache by scanning the source directory for playlist files (*.m3u8).
//
// Returns:
//   - error: An error, if any, encountered during the refresh process.
//
// Example usage:
//
//	myCache := // initialize your Cache
//	err := myCache.refresh()
//	if err != nil {
//	    // handle the error
//	}
func (cache *Cache) refresh() error {
	files, err := utils.GetFiles(cache.src, "*.m3u8")
	if err != nil {
		return err
	}

	for _, entry := range files {
		cache.add(entry)
	}

	return nil
}

// add adds a playlist file to the cache if it doesn't already exist.
//
// Parameters:
//   - path: The path to the playlist file to add.
//
// Returns:
//   - error: An error, if any, encountered during the addition process.
//
// Example usage:
//
//	myCache := // initialize your Cache
//	playlistPath := "/path/to/playlist.m3u8"
//	err := myCache.add(playlistPath)
//	if err != nil {
//	    // handle the error
//	}
func (cache *Cache) add(path string) error {

	file, err := os.Open(path)
	if err != nil {
		return nil
	}
	defer file.Close()

	name := strings.Split(filepath.ToSlash(path), "/")[3]

	if _, ok := cache.playlists[name]; !ok {
		playlist, err := hls.Load(file)
		if err != nil {
			return err
		}
		cache.playlists[name] = playlist
		log.Printf("[DEBUG] Added %s (%s) to cache\n", path, name)
	}

	return nil
}

// Refresh updates the cache in a thread-safe manner by acquiring a lock before calling the underlying refresh method.
//
// Returns:
//   - error: An error, if any, encountered during the refresh process.
//
// Example usage:
//
//	myCache := // initialize your Cache
//	err := myCache.Refresh()
//	if err != nil {
//	    // handle the error
//	}
func (cache *Cache) Refresh() error {
	cache.mutex.Lock()
	defer cache.mutex.Unlock()
	return cache.refresh()
}

// Keys retrieves the keys (playlist names) from the cache in a thread-safe manner.
// The keys are sorted in lexicographical order before being returned.
//
// Returns:
//   - []string: A sorted slice containing the keys (playlist names) from the cache.
//
// Example usage:
//
//	myCache := // initialize your Cache
//	playlistKeys := myCache.Keys()
func (cache *Cache) Keys() []string {
	cache.mutex.RLock()
	keys := utils.Keys[string, *hls.Playlist](cache.playlists)
	cache.mutex.RUnlock()
	slices.Sort(keys)
	return keys
}

// Get retrieves a playlist from the cache based on the provided ID.
//
// Parameters:
//   - id: The ID (playlist name) to retrieve from the cache.
//
// Returns:
//   - hls.Playlist: The playlist associated with the provided ID.
//   - error: An error, if any, encountered during the retrieval process.
//
// Example usage:
//
//	myCache := // initialize your Cache
//	playlistID := "example_playlist"
//	playlist, err := myCache.Get(playlistID)
//	if err != nil {
//	    // handle the error
//	}
func (cache *Cache) Get(id string) (hls.Playlist, error) {
	cache.mutex.RLock()
	defer cache.mutex.RUnlock()

	val, ok := cache.playlists[id]
	if !ok {
		return hls.Playlist{}, fmt.Errorf("%s was not found", id)
	}
	return *val, nil
}
