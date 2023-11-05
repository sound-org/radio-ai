package reader

import (
	"fmt"
	"io/fs"
	"log"
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/sound-org/radio-ai/server/internal/hls"
)

const maxFileLifespan = 2 // in days
// hls main streaming file configs
const version = 3
const beginSequence = 0
const enableCache = "NO"
const maxDuration = 11
const maxCapacity = 30

func getFiles(path, pattern string) ([]string, error) {
	var paths []string

	err := filepath.Walk(path, func(path string, info fs.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			return nil
		}
		if matched, err := filepath.Match(pattern, filepath.Base(path)); err != nil {
			return err
		} else if matched {
			paths = append(paths, path)
		}
		return nil
	})
	if err != nil {
		return nil, err
	}

	return paths, nil
}

type Manager struct {
	ReadRecords   map[string]*hls.Playlist
	WriteRecord   hls.Playlist
	StreamingFile *os.File
	Mutex         *sync.RWMutex
}

func (man *Manager) addRecord(path string) int {
	file, err := os.Open(path)
	if err != nil {
		return len(man.ReadRecords)
	}
	defer file.Close()

	record, err := hls.Load(file)
	if err != nil {
		return len(man.ReadRecords)
	}

	man.ReadRecords[path] = record

	return len(man.ReadRecords)
}

func (man *Manager) delete() {
	for key := range man.ReadRecords {
		if man.ReadRecords[key].ToDelete {
			delete(man.ReadRecords, key)
			root := filepath.Dir(key)
			err := os.RemoveAll(root)
			if err != nil {
				log.Println(err)
			}
		}
	}
}

func (man *Manager) markToDelete() {
	today := time.Now()
	for key := range man.ReadRecords {
		entry, err := os.Stat(key)
		if err == nil {
			if isToDelete(today, entry.ModTime(), maxFileLifespan) {
				man.ReadRecords[key].ToDelete = true
			}
		}
	}
}

func isToDelete(today, fileCreationDate time.Time, maxLifeSpan int) bool {
	// return true if file is older than lifespan
	return fileCreationDate.Add(time.Duration(maxLifeSpan) * 24 * time.Hour).Before(today)
}

func CreateManager(path, streamingName string, mutex *sync.RWMutex) (*Manager, error) {
	paths, err := getFiles(path, "*.m3u8")
	if err != nil {
		return nil, fmt.Errorf("path %v does not contain any subdirectory", path)
	}

	file, err := os.Create(streamingName)
	if err != nil {
		return nil, err
	}

	manager := Manager{
		ReadRecords: make(map[string]*hls.Playlist),
		WriteRecord: hls.Playlist{
			Metadata: hls.Metadata{
				Version:  version,
				Sequence: beginSequence,
				Cache:    enableCache,
				Duration: maxDuration,
			},
			Ts:       make([]hls.TsFile, maxCapacity),
			HasEnd:   false,
			ToDelete: false,
		},
		StreamingFile: file,
		Mutex:         mutex,
	}

	for _, entry := range paths {
		manager.addRecord(entry)
	}

	return &manager, nil
}
