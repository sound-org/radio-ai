package reader

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/sound-org/radio-ai/server/internal/hls"
)

const maxFileLifespan = 2 // in days

func GetDirectories(path string) []string {
	entries, err := os.ReadDir(path)
	if err != nil {
		return nil
	}
	var names []string

	for _, entry := range entries {
		if entry.IsDir() {
			names = append(names, entry.Name())
		}
	}

	return names
}

type Manager struct {
	ReadRecords   map[string]*hls.Record
	WriteRecord   hls.Record
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

func CreateManager(path string) (*Manager, error) {
	dirs := GetDirectories(path)
	if len(dirs) == 0 {
		return nil, fmt.Errorf("path %v does not contain any subdirectory", path)
	}

	return &Manager{}, nil
}
