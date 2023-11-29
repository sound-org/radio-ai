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

type Cache struct {
	src       string
	playlists map[string]*hls.Playlist
	mutex     *sync.RWMutex
}

func CreateCache(src string, mutex *sync.RWMutex) *Cache {
	return &Cache{
		src:       src,
		playlists: make(map[string]*hls.Playlist),
		mutex:     mutex,
	}
}

func (cache *Cache) refresh() error {
	files, err := utils.GetFiles(cache.src, "*.m3u8")
	if err != nil {
		return err
	}

	for _, entry := range files {
		log.Printf("[DEBUG] Refreshig... %s \n", entry)
		cache.add(entry)
	}

	return nil
}

func (cache *Cache) add(path string) error {

	file, err := os.Open(path)
	if err != nil {
		return nil
	}
	defer file.Close()

	//name := strings.TrimLeft(filepath.Dir(path), cache.src) for some reason it is not deterministic! >:-( 
	name := strings.Split(path, "/")[3]
	log.Printf("[DEBUG] Adding key %s for path %s (%s)\n", name, filepath.Dir(path), cache.src)

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

func (cache *Cache) Refresh() error {
	cache.mutex.Lock()
	defer cache.mutex.Unlock()

	return cache.refresh()
}

func (cache *Cache) Keys() []string {
	cache.mutex.RLock()
	defer cache.mutex.RUnlock()
	keys := utils.Keys[string, *hls.Playlist](cache.playlists)
	slices.Sort(keys)
	return keys
}

func (cache *Cache) Get(id string) (hls.Playlist, error) {
	cache.mutex.RLock()
	defer cache.mutex.RUnlock()

	val, ok := cache.playlists[id]
	if !ok {
		return hls.Playlist{}, fmt.Errorf("%s was not found", id)
	}
	return *val, nil
}
